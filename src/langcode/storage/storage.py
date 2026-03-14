"""Legacy JSON file storage with migrations."""

import json
import os
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import TypeVar

from langcode.util.filesystem import Filesystem
from langcode.util.glob import Glob
from langcode.util.lock import Lock
from langcode.util.log import Log

T = TypeVar("T")

log = Log.create(service="storage")


class NotFoundError(Exception):
    """Resource not found in storage."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class Storage:
    """Legacy JSON file storage system."""

    _state = None

    @staticmethod
    async def _run_migrations(dir: str):
        """Run storage migrations."""
        from langcode.util.git import git

        # Migration 0: Migrate old project structure
        async def migration_0(dir: str):
            project_dir = Path(dir).parent / "project"
            if not await Filesystem.is_dir(str(project_dir)):
                return

            project_dirs = await Glob.scan("*", cwd=str(project_dir), include="all")

            for project_name in project_dirs:
                full_path = project_dir / project_name
                if not await Filesystem.is_dir(str(full_path)):
                    continue

                log.info(f"migrating project {project_name}")
                project_id = project_name
                worktree = "/"

                if project_id != "global":
                    # Find worktree from message files
                    msg_files = await Glob.scan(
                        "storage/session/message/*/*.json",
                        cwd=str(full_path),
                        absolute=True,
                    )

                    for msg_file in msg_files:
                        json_data = await Filesystem.read_json(msg_file)
                        worktree = json_data.get("path", {}).get("root")
                        if worktree:
                            break

                    if not worktree:
                        continue
                    if not await Filesystem.is_dir(worktree):
                        continue

                    # Get git root commit as project ID
                    result = await git(["rev-list", "--max-parents=0", "--all"], cwd=worktree)
                    commits = [line.strip() for line in result.text().split("\n") if line.strip()]
                    commits.sort()
                    if not commits:
                        continue

                    project_id = commits[0]

                    # Write project metadata
                    import time

                    now = int(time.time() * 1000)
                    await Filesystem.write_json(
                        os.path.join(dir, "project", f"{project_id}.json"),
                        {
                            "id": project_id,
                            "vcs": "git",
                            "worktree": worktree,
                            "time": {
                                "created": now,
                                "initialized": now,
                            },
                        },
                    )

                    log.info(f"migrating sessions for project {project_id}")

                    # Migrate sessions
                    session_files = await Glob.scan(
                        "storage/session/info/*.json",
                        cwd=str(full_path),
                        absolute=True,
                    )

                    for session_file in session_files:
                        dest = os.path.join(dir, "session", project_id, Path(session_file).name)
                        log.info("copying", session_file=session_file, dest=dest)
                        session = await Filesystem.read_json(session_file)
                        await Filesystem.write_json(dest, session)

                        log.info(f"migrating messages for session {session['id']}")

                        # Migrate messages
                        msg_files = await Glob.scan(
                            f"storage/session/message/{session['id']}/*.json",
                            cwd=str(full_path),
                            absolute=True,
                        )

                        for msg_file in msg_files:
                            dest = os.path.join(dir, "message", session["id"], Path(msg_file).name)
                            log.info("copying", msg_file=msg_file, dest=dest)
                            message = await Filesystem.read_json(msg_file)
                            await Filesystem.write_json(dest, message)

                            log.info(f"migrating parts for message {message['id']}")

                            # Migrate parts
                            part_files = await Glob.scan(
                                f"storage/session/part/{session['id']}/{message['id']}/*.json",
                                cwd=str(full_path),
                                absolute=True,
                            )

                            for part_file in part_files:
                                dest = os.path.join(dir, "part", message["id"], Path(part_file).name)
                                part = await Filesystem.read_json(part_file)
                                log.info("copying", part_file=part_file, dest=dest)
                                await Filesystem.write_json(dest, part)

        # Migration 1: Extract diffs from session summaries
        async def migration_1(dir: str):
            session_files = await Glob.scan("session/*/*.json", cwd=dir, absolute=True)

            for item in session_files:
                session = await Filesystem.read_json(item)
                if not session.get("projectID"):
                    continue
                if not session.get("summary", {}).get("diffs"):
                    continue

                diffs = session["summary"]["diffs"]
                await Filesystem.write(
                    os.path.join(dir, "session_diff", f"{session['id']}.json"),
                    json.dumps(diffs),
                )

                # Update session with aggregated summary
                additions = sum(d.get("additions", 0) for d in diffs)
                deletions = sum(d.get("deletions", 0) for d in diffs)

                await Filesystem.write_json(
                    os.path.join(dir, "session", session["projectID"], f"{session['id']}.json"),
                    {
                        **session,
                        "summary": {"additions": additions, "deletions": deletions},
                    },
                )

        migrations = [migration_0, migration_1]

        # Read current migration version
        migration_file = os.path.join(dir, "migration")
        try:
            migration_version = int(await Filesystem.read_json(migration_file))
        except Exception:
            migration_version = 0

        # Run pending migrations
        for index in range(migration_version, len(migrations)):
            log.info("running migration", index=index)
            try:
                await migrations[index](dir)
                await Filesystem.write(migration_file, str(index + 1))
            except Exception as e:
                log.error("failed to run migration", index=index, error=str(e))

    @staticmethod
    async def _get_state():
        """Initialize storage state."""
        if Storage._state is not None:
            return Storage._state

        from langcode.global_config import Global

        dir = os.path.join(Global.Path.data, "storage")
        await Storage._run_migrations(dir)
        Storage._state = {"dir": dir}
        return Storage._state

    @staticmethod
    async def remove(key: list[str]):
        """Remove a storage entry."""
        state = await Storage._get_state()
        dir = state["dir"]
        target = os.path.join(dir, *key) + ".json"

        async def _remove():
            try:
                os.unlink(target)
            except FileNotFoundError:
                pass

        return await Storage._with_error_handling(_remove)

    @staticmethod
    async def read(key: list[str]) -> T:
        """Read a storage entry."""
        state = await Storage._get_state()
        dir = state["dir"]
        target = os.path.join(dir, *key) + ".json"

        async def _read():
            async with Lock.read(target):
                result = await Filesystem.read_json(target)
                return result

        return await Storage._with_error_handling(_read)

    @staticmethod
    async def update(key: list[str], fn: Callable[[T], None]) -> T:
        """Update a storage entry."""
        state = await Storage._get_state()
        dir = state["dir"]
        target = os.path.join(dir, *key) + ".json"

        async def _update():
            async with Lock.write(target):
                content = await Filesystem.read_json(target)
                fn(content)
                await Filesystem.write_json(target, content)
                return content

        return await Storage._with_error_handling(_update)

    @staticmethod
    async def write(key: list[str], content: T):
        """Write a storage entry."""
        state = await Storage._get_state()
        dir = state["dir"]
        target = os.path.join(dir, *key) + ".json"

        async def _write():
            async with Lock.write(target):
                await Filesystem.write_json(target, content)

        return await Storage._with_error_handling(_write)

    @staticmethod
    async def _with_error_handling(body: Callable[[], Awaitable[T]]) -> T:
        """Execute with error handling."""
        try:
            return await body()
        except FileNotFoundError as e:
            raise NotFoundError(f"Resource not found: {e.filename}") from None
        except Exception:
            raise

    @staticmethod
    async def list(prefix: list[str]) -> list[list[str]]:
        """List storage entries with given prefix."""
        state = await Storage._get_state()
        dir = state["dir"]

        try:
            results = await Glob.scan("**/*", cwd=os.path.join(dir, *prefix), include="file")
            # Convert paths to key lists, removing .json extension
            keys = []
            for result in results:
                parts = result[:-5].split(os.sep)  # Remove .json
                keys.append([*prefix, *parts])
            keys.sort()
            return keys
        except Exception:
            return []
