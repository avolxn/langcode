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
