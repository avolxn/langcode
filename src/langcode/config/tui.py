"""TUI configuration management."""

from typing import Any

import anyio

from langcode.config.flag import Flag
from langcode.config.globals import Global
from langcode.config.paths import ConfigPaths
from langcode.config.tui_schema import TuiInfo
from langcode.util.log import Log

log = Log.create(service="tui.config")


class TuiConfig:
    """TUI configuration loader and manager."""

    Info = TuiInfo

    _state: dict[str, Any] | None = None

    @classmethod
    def _custom_path(cls) -> str | None:
        """Get custom TUI config path from flag."""
        return Flag.OPENCODE_TUI_CONFIG

    @classmethod
    async def _load_file(cls, filepath: str) -> dict[str, Any]:
        """Load TUI config from a file.

        Args:
            filepath: Path to config file

        Returns:
            Parsed configuration dictionary
        """
        text = await ConfigPaths.read_file(filepath)
        if not text:
            return {}

        try:
            return await cls._load(text, filepath)
        except Exception as error:
            log.warn("failed to load tui config", path=filepath, error=error)
            return {}

    @classmethod
    async def _load(cls, text: str, config_filepath: str) -> dict[str, Any]:
        """Parse and validate TUI configuration text.

        Args:
            text: Configuration text
            config_filepath: Path to config file (for error messages)

        Returns:
            Validated configuration dictionary
        """
        data = await ConfigPaths.parse_text(text, config_filepath, "empty")
        if not data or not isinstance(data, dict) or isinstance(data, list):
            return {}

        # Flatten a nested "tui" key so users who wrote `{ "tui": { ... } }` inside tui.json
        # (mirroring the old opencode.json shape) still get their settings applied.
        normalized = dict(data)
        if "tui" in normalized:
            tui_data = normalized.pop("tui")
            if isinstance(tui_data, dict):
                # Merge tui data, with top-level keys taking precedence
                normalized = {**tui_data, **normalized}

        try:
            parsed = TuiInfo.model_validate(normalized)
            return parsed.model_dump(exclude_none=True, by_alias=True)
        except Exception as error:
            log.warn("invalid tui config", path=config_filepath, error=error)
            return {}

    @classmethod
    def _merge_info(cls, target: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
        """Deep merge two TUI config dictionaries.

        Args:
            target: Target dictionary
            source: Source dictionary to merge in

        Returns:
            Merged dictionary
        """
        from langcode.util.merge import merge_deep

        return merge_deep(target, source)

    @classmethod
    async def get(cls) -> dict[str, Any]:
        """Get the current TUI configuration.

        Returns:
            Complete TUI configuration
        """
        if cls._state is not None:
            return cls._state

        # Import here to avoid circular dependency
        from langcode.config.config import Config

        # Get directories
        directories: list[str] = []
        custom = cls._custom_path()
        managed = Config.managed_config_dir()

        result: dict[str, Any] = {}

        # Load global config
        for file in ConfigPaths.file_in_directory(Global.Path.config, "tui"):
            result = cls._merge_info(result, await cls._load_file(file))

        # Load custom config
        if custom:
            result = cls._merge_info(result, await cls._load_file(custom))
            log.debug("loaded custom tui config", path=custom)

        # Load project files (simplified - full implementation would use Instance)
        # project_files = await ConfigPaths.project_files("tui", directory, worktree)
        # for file in project_files:
        #     result = cls._merge_info(result, await cls._load_file(file))

        # Load from .opencode directories
        for dir_path in directories:
            if not dir_path.endswith(".opencode") and dir_path != Flag.OPENCODE_CONFIG_DIR:
                continue
            for file in ConfigPaths.file_in_directory(dir_path, "tui"):
                result = cls._merge_info(result, await cls._load_file(file))

        # Load managed config
        if await anyio.Path(managed).exists():
            for file in ConfigPaths.file_in_directory(managed, "tui"):
                result = cls._merge_info(result, await cls._load_file(file))

        # Parse keybinds with defaults (simplified - full implementation would use Config.Keybinds)
        if "keybinds" not in result:
            result["keybinds"] = {}

        cls._state = result
        return result

    @classmethod
    def reset(cls) -> None:
        """Reset cached state."""
        cls._state = None
