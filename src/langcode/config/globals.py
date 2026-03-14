"""Global configuration paths and settings."""

import os
from pathlib import Path


APP = "langcode"


class _GlobalPath:
    """Global paths following XDG Base Directory specification."""

    @property
    def home(self) -> str:
        """Home directory (with test override support)."""
        return os.environ.get("LANGCODE_TEST_HOME", str(Path.home()))

    @property
    def data(self) -> str:
        """Data directory."""
        xdg_data = os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share"))
        return str(Path(xdg_data) / APP)

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
        xdg_cache = os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache"))
        return str(Path(xdg_cache) / APP)

    @property
    def config(self) -> str:
        """Config directory."""
        xdg_config = os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))
        return str(Path(xdg_config) / APP)

    @property
    def state(self) -> str:
        """State directory."""
        xdg_state = os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local" / "state"))
        return str(Path(xdg_state) / APP)

    def ensure_dirs(self) -> None:
        """Ensure all directories exist."""
        for dir_path in [self.data, self.bin, self.log, self.cache, self.config, self.state]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)


class Global:
    """Global configuration."""

    Path = _GlobalPath()


# Ensure directories exist on import
Global.Path.ensure_dirs()
