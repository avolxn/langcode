"""Glob pattern matching utilities."""

from typing import Literal

import anyio


class Glob:
    """Glob pattern matching.

    Provides file pattern matching with filtering and path conversion options.
    """

    @staticmethod
    async def scan(
        pattern: str,
        *,
        cwd: str | None = None,
        absolute: bool = False,
        include: Literal["all", "file", "dir"] = "all",
    ) -> list[str]:
        """Scan for files matching pattern.

        Args:
            pattern: Glob pattern (e.g., "*.txt", "**/*.py")
            cwd: Working directory for the scan
            absolute: Return absolute paths instead of relative
            include: Filter by type ("all", "file", or "dir")

        Returns:
            List of matching file paths
        """

        base_path = anyio.Path(cwd) if cwd else anyio.Path()

        paths = [p async for p in base_path.glob(pattern)]

        if include == "file":
            paths = [p for p in paths if await p.is_file()]
        elif include == "dir":
            paths = [p for p in paths if await p.is_dir()]

        if absolute:
            matches = [str(p) for p in paths]
        else:
            matches = [str(p.relative_to(base_path)) for p in paths]

        return matches
