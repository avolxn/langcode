"""Global configuration paths and settings."""

from pathlib import Path


class Global:
    """Global configuration."""

    class Path:
        """Global paths."""

        # Data directory for storage
        data: str = str(Path("~/.langcode").expanduser())

        @classmethod
        def ensure_dirs(cls):
            """Ensure all directories exist."""
            Path(cls.data).mkdir(parents=True, exist_ok=True)


# Ensure directories exist on import
Global.Path.ensure_dirs()
