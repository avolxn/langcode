"""JSON file storage."""

from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import TypeVar

import anyio

from langcode.util.filesystem import Filesystem
from langcode.util.glob import Glob
from langcode.util.lock import Lock
from langcode.util.log import Log

T = TypeVar("T")

log = Log.create(service="storage")


class NotFoundError(Exception):
    """Resource not found in storage.

    Attributes:
        message: Error message describing what was not found
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class Storage:
    """JSON file storage system.

    Provides JSON-based storage for all data.
    All data is stored as editable JSON files in ~/.langcode/storage/

    Attributes:
        _state: Cached storage state containing directory path
    """

    _state = None

    @staticmethod
    async def _get_state():
        """Initialize storage state.

        Returns:
            Dictionary containing storage directory path
        """
        if Storage._state is not None:
            return Storage._state

        from langcode.global_config import Global

        dir = str(Path(Global.Path.data) / "storage")
        Storage._state = {"dir": dir}
        return Storage._state

    @staticmethod
    async def remove(key: list[str]):
        """Remove a storage entry.

        Args:
            key: Path components to the storage entry (e.g., ["project", "id"])
        """
        state = await Storage._get_state()
        dir = state["dir"]
        target = str(Path(dir).joinpath(*key)) + ".json"

        async def _remove():
            try:
                await anyio.Path(target).unlink()
            except FileNotFoundError:
                pass

        return await Storage._with_error_handling(_remove)

    @staticmethod
    async def read(key: list[str]) -> T:
        """Read a storage entry.

        Args:
            key: Path components to the storage entry

        Returns:
            Parsed JSON data from the storage file

        Raises:
            NotFoundError: If the storage entry does not exist
        """
        state = await Storage._get_state()
        dir = state["dir"]
        target = str(Path(dir).joinpath(*key)) + ".json"

        async def _read():
            async with Lock.read(target):
                result = await Filesystem.read_json(target)
                return result

        return await Storage._with_error_handling(_read)

    @staticmethod
    async def update(key: list[str], fn: Callable[[T], None]) -> T:
        """Update a storage entry.

        Args:
            key: Path components to the storage entry
            fn: Function that modifies the data in-place

        Returns:
            Updated data after applying the function

        Raises:
            NotFoundError: If the storage entry does not exist
        """
        state = await Storage._get_state()
        dir = state["dir"]
        target = str(Path(dir).joinpath(*key)) + ".json"

        async def _update():
            async with Lock.write(target):
                content = await Filesystem.read_json(target)
                fn(content)
                await Filesystem.write_json(target, content)
                return content

        return await Storage._with_error_handling(_update)

    @staticmethod
    async def write(key: list[str], content: T):
        """Write a storage entry.

        Args:
            key: Path components to the storage entry
            content: Data to write (will be JSON serialized)
        """
        state = await Storage._get_state()
        dir = state["dir"]
        target = str(Path(dir).joinpath(*key)) + ".json"

        async def _write():
            async with Lock.write(target):
                await Filesystem.write_json(target, content)

        return await Storage._with_error_handling(_write)

    @staticmethod
    async def _with_error_handling(body: Callable[[], Awaitable[T]]) -> T:
        """Execute with error handling.

        Args:
            body: Async function to execute

        Returns:
            Result from the body function

        Raises:
            NotFoundError: If a FileNotFoundError occurs
        """
        try:
            return await body()
        except FileNotFoundError as e:
            raise NotFoundError(f"Resource not found: {e.filename}") from None
        except Exception:
            raise

    @staticmethod
    async def list(prefix: list[str]) -> list[list[str]]:
        """List storage entries with given prefix.

        Args:
            prefix: Path prefix to filter entries

        Returns:
            List of key paths matching the prefix
        """
        state = await Storage._get_state()
        dir = state["dir"]

        try:
            results = await Glob.scan("**/*", cwd=str(Path(dir).joinpath(*prefix)), include="file")
            # Convert paths to key lists, removing .json extension
            keys = []
            for result in results:
                parts = list(Path(result).with_suffix("").parts)
                keys.append([*prefix, *parts])
            keys.sort()
            return keys
        except Exception:
            return []
