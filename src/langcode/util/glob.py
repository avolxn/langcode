"""Glob pattern matching utilities."""

import glob as stdlib_glob
import os
from pathlib import Path
from typing import Literal


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
        # Use pathlib to avoid changing global cwd
        matches: list[str]
        if cwd:
            base_path = Path(cwd)
            path_matches = list(base_path.glob(pattern))  # noqa: ASYNC240
            # Convert Path objects to strings
            matches = [str(m.relative_to(base_path)) for m in path_matches]
        else:
            matches = stdlib_glob.glob(pattern, recursive=True)

        # Filter by type
        if include == "file":
            if cwd:
                matches = [m for m in matches if (Path(cwd) / m).is_file()]
            else:
                matches = [m for m in matches if os.path.isfile(m)]  # noqa: ASYNC240
        elif include == "dir":
            if cwd:
                matches = [m for m in matches if (Path(cwd) / m).is_dir()]
            else:
                matches = [m for m in matches if os.path.isdir(m)]  # noqa: ASYNC240

        # Convert to absolute paths if requested
        if absolute and cwd:
            matches = [str(Path(cwd) / m) for m in matches]
        elif absolute:
            matches = [os.path.abspath(m) for m in matches]  # noqa: ASYNC240

        return matches
