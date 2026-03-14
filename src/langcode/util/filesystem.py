"""Filesystem utilities."""

import json
from pathlib import Path
from typing import Any, TypeVar

import aiofiles
import anyio

T = TypeVar("T")


class Filesystem:
    """Filesystem operations.

    Provides async file I/O operations for JSON and text files.
    """

    @staticmethod
    async def read_json(path: str) -> Any:
        """Read JSON file.

        Args:
            path: Path to the JSON file

        Returns:
            Parsed JSON data
        """
        async with aiofiles.open(path) as f:
            content = await f.read()
            return json.loads(content)

    @staticmethod
    async def write_json(path: str, data: Any):
        """Write JSON file.

        Args:
            path: Path to the JSON file
            data: Data to serialize as JSON
        """
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(path, "w") as f:
            await f.write(json.dumps(data, indent=2))

    @staticmethod
    async def write(path: str, content: str):
        """Write text file.

        Args:
            path: Path to the text file
            content: Text content to write
        """
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(path, "w") as f:
            await f.write(content)

    @staticmethod
    async def read(path: str) -> str:
        """Read text file.

        Args:
            path: Path to the text file

        Returns:
            File contents as string
        """
        async with aiofiles.open(path) as f:
            return await f.read()

    @staticmethod
    async def is_dir(path: str) -> bool:
        """Check if path is a directory.

        Args:
            path: Path to check

        Returns:
            True if path is a directory, False otherwise
        """
        return await anyio.Path(path).is_dir()

    @staticmethod
    async def read_text(path: str) -> str:
        """Read text file (alias for read).

        Args:
            path: Path to the text file

        Returns:
            File contents as string
        """
        return await Filesystem.read(path)

    @staticmethod
    async def exists(path: str) -> bool:
        """Check if path exists.

        Args:
            path: Path to check

        Returns:
            True if path exists, False otherwise
        """
        return await anyio.Path(path).exists()

    @staticmethod
    async def find_up(
        filename: str,
        start: str,
        stop: str,
    ) -> list[str]:
        """Find files by searching up the directory tree.

        Args:
            filename: Name of file to find
            start: Starting directory
            stop: Stop directory (inclusive)

        Returns:
            List of found file paths
        """
        found: list[str] = []
        current = Path(start).resolve()
        stop_path = Path(stop).resolve()

        while True:
            candidate = current / filename
            if await anyio.Path(candidate).exists():
                found.append(str(candidate))

            if current == stop_path:
                break

            parent = current.parent
            if parent == current:  # Reached root
                break

            current = parent

        return found

    @staticmethod
    async def up(
        targets: list[str],
        start: str,
        stop: str,
    ):
        """Iterate up directory tree finding target directories.

        Args:
            targets: List of directory names to find
            start: Starting directory
            stop: Stop directory (inclusive)

        Yields:
            Paths to found directories
        """
        current = Path(start).resolve()
        stop_path = Path(stop).resolve()

        while True:
            for target in targets:
                candidate = current / target
                if await anyio.Path(candidate).is_dir():
                    yield str(candidate)

            if current == stop_path:
                break

            parent = current.parent
            if parent == current:  # Reached root
                break

            current = parent
