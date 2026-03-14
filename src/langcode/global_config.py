"""Global configuration paths and settings."""

import os
from pathlib import Path


class Global:
    """Global configuration."""

    class Path:
        """Global paths."""

        # Data directory for storage
        data: str = os.path.expanduser("~/.langcode")

        @classmethod
        def ensure_dirs(cls):
            """Ensure all directories exist."""
            Path(cls.data).mkdir(parents=True, exist_ok=True)


# Ensure directories exist on import
Global.Path.ensure_dirs()
