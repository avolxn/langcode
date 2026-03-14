"""Global configuration paths and settings."""

import os
from pathlib import Path


def _xdg_data_home() -> str:
    """Get XDG data directory."""
    return os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share"))


def _xdg_cache_home() -> str:
    """Get XDG cache directory."""
    return os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache"))


def _xdg_config_home() -> str:
    """Get XDG config directory."""
    return os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))


def _xdg_state_home() -> str:
    """Get XDG state directory."""
    return os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local" / "state"))


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
        return str(Path(_xdg_data_home()) / APP)

    @property
    def bin(self) -> str:
        """Binary directory."""
        return str(Path(_xdg_data_home()) / APP / "bin")

    @property
    def log(self) -> str:
        """Log directory."""
        return str(Path(_xdg_data_home()) / APP / "log")

    @property
    def cache(self) -> str:
        """Cache directory."""
        return str(Path(_xdg_cache_home()) / APP)

    @property
    def config(self) -> str:
        """Config directory."""
        return str(Path(_xdg_config_home()) / APP)

    @property
    def state(self) -> str:
        """State directory."""
        return str(Path(_xdg_state_home()) / APP)

    def ensure_dirs(self) -> None:
        """Ensure all directories exist."""
        for dir_path in [self.data, self.bin, self.log, self.cache, self.config, self.state]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)


class Global:
    """Global configuration."""

    Path = _GlobalPath()


# Ensure directories exist on import
Global.Path.ensure_dirs()
