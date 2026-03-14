"""File locking utilities."""

import fcntl
import hashlib
import os
from pathlib import Path


class Lock:
    """File lock context manager."""

    def __init__(self, path: str, exclusive: bool = False):
        self.path = path
        self.exclusive = exclusive
        self.fd: int | None = None
        # Use a separate lock directory to avoid interfering with data files
        self.lock_file = self._get_lock_file(path)

    def _get_lock_file(self, path: str) -> str:
        """Get lock file path in a separate directory."""
        # Create a hash of the path to use as lock filename
        path_hash = hashlib.md5(path.encode(), usedforsecurity=False).hexdigest()  # noqa: S324
        lock_dir = Path.home() / ".langcode" / "locks"
        lock_dir.mkdir(parents=True, exist_ok=True)
        return str(lock_dir / f"{path_hash}.lock")

    async def __aenter__(self):
        """Acquire lock."""
        # Ensure parent directory of actual file exists
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)

        # Open lock file for locking
        self.fd = os.open(self.lock_file, os.O_RDWR | os.O_CREAT)

        # Acquire lock
        lock_type = fcntl.LOCK_EX if self.exclusive else fcntl.LOCK_SH
        fcntl.flock(self.fd, lock_type)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Release lock."""
        if self.fd is not None:
            fcntl.flock(self.fd, fcntl.LOCK_UN)
            os.close(self.fd)
            self.fd = None

    @staticmethod
    def read(path: str) -> "Lock":
        """Create a read lock."""
        return Lock(path, exclusive=False)

    @staticmethod
    def write(path: str) -> "Lock":
        """Create a write lock."""
        return Lock(path, exclusive=True)
