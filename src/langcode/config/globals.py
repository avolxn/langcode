"""Global configuration paths and settings."""

from pathlib import Path

APP = "langcode"


class _GlobalPath:
    """Global paths for LangCode."""

    @property
    def home(self) -> str:
        """Home directory (with test override support)."""
        return str(Path.home())

    @property
    def data(self) -> str:
        """Data directory."""
        return str(Path(self.home) / f".{APP}")

    @property
    def bin(self) -> str:
        """Binary directory."""
        return str(Path(self.data) / "bin")

    @property
    def log(self) -> str:
        """Log directory."""
        return str(Path(self.data) / "log")

    @property
    def cache(self) -> str:
        """Cache directory."""
        return str(Path(self.data) / "cache")

    @property
    def config(self) -> str:
        """Config directory."""
        return str(Path(self.data) / "config")

    @property
    def state(self) -> str:
        """State directory."""
        return str(Path(self.data) / "state")

    def ensure_dirs(self) -> None:
        """Ensure all directories exist."""
        for dir_path in [self.data, self.bin, self.log, self.cache, self.config, self.state]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)


class Global:
    """Global configuration."""

    Path = _GlobalPath()


Global.Path.ensure_dirs()
