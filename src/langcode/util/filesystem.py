"""Filesystem utilities."""

import json
import os
from pathlib import Path
from typing import Any, TypeVar

import aiofiles

T = TypeVar("T")


class Filesystem:
    """Filesystem operations."""

    @staticmethod
    async def read_json(path: str) -> Any:
        """Read JSON file."""
        async with aiofiles.open(path) as f:
            content = await f.read()
            return json.loads(content)

    @staticmethod
    async def write_json(path: str, data: Any):
        """Write JSON file."""
        # Ensure directory exists
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(path, "w") as f:
            await f.write(json.dumps(data, indent=2))

    @staticmethod
    async def write(path: str, content: str):
        """Write text file."""
        # Ensure directory exists
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(path, "w") as f:
            await f.write(content)

    @staticmethod
    async def read(path: str) -> str:
        """Read text file."""
        async with aiofiles.open(path) as f:
            return await f.read()

    @staticmethod
    async def is_dir(path: str) -> bool:
        """Check if path is a directory."""
        return os.path.isdir(path)  # noqa: ASYNC240
