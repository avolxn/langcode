"""Glob pattern matching utilities."""

import glob as stdlib_glob
import os
from typing import Literal


class Glob:
    """Glob pattern matching."""

    @staticmethod
    async def scan(
        pattern: str,
        *,
        cwd: str | None = None,
        absolute: bool = False,
        include: Literal["all", "file", "dir"] = "all",
    ) -> list[str]:
        """Scan for files matching pattern."""
        if cwd:
            original_cwd = os.getcwd()
            os.chdir(cwd)
        else:
            original_cwd = None

        try:
            matches = stdlib_glob.glob(pattern, recursive=True)

            # Filter by type
            if include == "file":
                matches = [m for m in matches if os.path.isfile(m)]  # noqa: ASYNC240
            elif include == "dir":
                matches = [m for m in matches if os.path.isdir(m)]  # noqa: ASYNC240

            # Convert to absolute paths if requested
            if absolute and cwd:
                matches = [os.path.join(cwd, m) for m in matches]
            elif absolute:
                matches = [os.path.abspath(m) for m in matches]  # noqa: ASYNC240

            return matches
        finally:
            if original_cwd:
                os.chdir(original_cwd)
