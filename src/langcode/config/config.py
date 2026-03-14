"""Main configuration management for LangCode."""

import getpass
import os
import sys
from pathlib import Path
from typing import Any, Literal

import anyio
from pydantic import BaseModel, Field

from langcode.config.flag import Flag
from langcode.config.globals import Global
from langcode.config.paths import ConfigPaths
from langcode.util.filesystem import Filesystem
from langcode.util.log import Log
from langcode.util.merge import merge_deep

log = Log.create(service="config")


class PermissionAction(BaseModel):
    """Permission action type."""

    action: Literal["ask", "allow", "deny"]


class McpLocal(BaseModel):
    """Local MCP server configuration."""

    type: Literal["local"] = Field(description="Type of MCP server connection")
    command: list[str] = Field(description="Command and arguments to run the MCP server")
    environment: dict[str, str] | None = Field(
        None,
        description="Environment variables to set when running the MCP server",
    )
    enabled: bool | None = Field(
        None,
        description="Enable or disable the MCP server on startup",
    )
    timeout: int | None = Field(
        None,
        gt=0,
        description="Timeout in ms for MCP server requests. Defaults to 5000 (5 seconds) if not specified.",
    )

    class Config:
        extra = "forbid"


class McpOAuth(BaseModel):
    """OAuth configuration for MCP."""

    client_id: str | None = Field(
        None,
        alias="clientId",
        description="OAuth client ID. If not provided, dynamic client registration (RFC 7591) will be attempted.",
    )
    client_secret: str | None = Field(
        None,
        alias="clientSecret",
        description="OAuth client secret (if required by the authorization server)",
    )
    scope: str | None = Field(
        None,
        description="OAuth scopes to request during authorization",
    )

    class Config:
        extra = "forbid"
        populate_by_name = True


class McpRemote(BaseModel):
    """Remote MCP server configuration."""

    type: Literal["remote"] = Field(description="Type of MCP server connection")
    url: str = Field(description="URL of the remote MCP server")
    enabled: bool | None = Field(
        None,
        description="Enable or disable the MCP server on startup",
    )
    headers: dict[str, str] | None = Field(
        None,
        description="Headers to send with the request",
    )
    oauth: McpOAuth | Literal[False] | None = Field(
        None,
        description="OAuth authentication configuration for the MCP server. Set to false to disable OAuth auto-detection.",
    )
    timeout: int | None = Field(
        None,
        gt=0,
        description="Timeout in ms for MCP server requests. Defaults to 5000 (5 seconds) if not specified.",
    )

    class Config:
        extra = "forbid"


class Command(BaseModel):
    """Command configuration."""

    template: str
    description: str | None = None
    agent: str | None = None
    model: str | None = None
    subtask: bool | None = None


class Skills(BaseModel):
    """Skills configuration."""

    paths: list[str] | None = Field(
        None,
        description="Additional paths to skill folders",
    )
    urls: list[str] | None = Field(
        None,
        description="URLs to fetch skills from (e.g., https://example.com/.well-known/skills/)",
    )


class Agent(BaseModel):
    """Agent configuration."""

    model: str | None = None
    variant: str | None = Field(
        None,
        description="Default model variant for this agent (applies only when using the agent's configured model).",
    )
    temperature: float | None = None
    top_p: float | None = None
    prompt: str | None = None
    tools: dict[str, bool] | None = Field(
        None,
        description="@deprecated Use 'permission' field instead",
    )
    disable: bool | None = None
    description: str | None = Field(
        None,
        description="Description of when to use the agent",
    )
    mode: Literal["subagent", "primary", "all"] | None = None
    hidden: bool | None = Field(
        None,
        description="Hide this subagent from the @ autocomplete menu (default: false, only applies to mode: subagent)",
    )
    options: dict[str, Any] | None = None
    color: str | None = Field(
        None,
        description="Hex color code (e.g., #FF5733) or theme color (e.g., primary)",
    )
    steps: int | None = Field(
        None,
        gt=0,
        description="Maximum number of agentic iterations before forcing text-only response",
    )
    max_steps: int | None = Field(
        None,
        gt=0,
        description="@deprecated Use 'steps' field instead.",
    )
    permission: dict[str, Any] | None = None

    class Config:
        extra = "allow"


class Server(BaseModel):
    """Server configuration."""

    port: int | None = Field(None, gt=0, description="Port to listen on")
    hostname: str | None = Field(None, description="Hostname to listen on")
    mdns: bool | None = Field(None, description="Enable mDNS service discovery")
    mdns_domain: str | None = Field(
        None,
        alias="mdnsDomain",
        description="Custom domain name for mDNS service (default: opencode.local)",
    )
    cors: list[str] | None = Field(
        None,
        description="Additional domains to allow for CORS",
    )

    class Config:
        extra = "forbid"
        populate_by_name = True


class Provider(BaseModel):
    """Provider configuration."""

    whitelist: list[str] | None = None
    blacklist: list[str] | None = None
    models: dict[str, Any] | None = None
    options: dict[str, Any] | None = None

    class Config:
        extra = "forbid"


class Compaction(BaseModel):
    """Compaction configuration."""

    auto: bool | None = Field(
        None,
        description="Enable automatic compaction when context is full (default: true)",
    )
    prune: bool | None = Field(
        None,
        description="Enable pruning of old tool outputs (default: true)",
    )
    reserved: int | None = Field(
        None,
        ge=0,
        description="Token buffer for compaction. Leaves enough window to avoid overflow during compaction.",
    )


class Experimental(BaseModel):
    """Experimental features configuration."""

    disable_paste_summary: bool | None = None
    batch_tool: bool | None = Field(None, description="Enable the batch tool")
    open_telemetry: bool | None = Field(
        None,
        alias="openTelemetry",
        description="Enable OpenTelemetry spans for AI SDK calls (using the 'experimental_telemetry' flag)",
    )
    primary_tools: list[str] | None = Field(
        None,
        description="Tools that should only be available to primary agents.",
    )
    continue_loop_on_deny: bool | None = Field(
        None,
        description="Continue the agent loop when a tool call is denied",
    )
    mcp_timeout: int | None = Field(
        None,
        gt=0,
        description="Timeout in milliseconds for model context protocol (MCP) requests",
    )

    class Config:
        populate_by_name = True


class ConfigInfo(BaseModel):
    """Complete configuration information."""

    schema_: str | None = Field(
        None,
        alias="$schema",
        description="JSON schema reference for configuration validation",
    )
    log_level: str | None = Field(None, alias="logLevel", description="Log level")
    server: Server | None = Field(
        None,
        description="Server configuration for opencode serve and web commands",
    )
    command: dict[str, Command] | None = Field(
        None,
        description="Command configuration, see https://opencode.ai/docs/commands",
    )
    skills: Skills | None = Field(
        None,
        description="Additional skill folder paths",
    )
    watcher: dict[str, Any] | None = None
    plugin: list[str] | None = None
    snapshot: bool | None = None
    share: Literal["manual", "auto", "disabled"] | None = Field(
        None,
        description="Control sharing behavior:'manual' allows manual sharing via commands, 'auto' enables automatic sharing, 'disabled' disables all sharing",
    )
    autoshare: bool | None = Field(
        None,
        description="@deprecated Use 'share' field instead. Share newly created sessions automatically",
    )
    autoupdate: bool | Literal["notify"] | None = Field(
        None,
        description="Automatically update to the latest version. Set to true to auto-update, false to disable, or 'notify' to show update notifications",
    )
    disabled_providers: list[str] | None = Field(
        None,
        description="Disable providers that are loaded automatically",
    )
    enabled_providers: list[str] | None = Field(
        None,
        description="When set, ONLY these providers will be enabled. All other providers will be ignored",
    )
    model: str | None = Field(
        None,
        description="Model to use in the format of provider/model, eg anthropic/claude-2",
    )
    small_model: str | None = Field(
        None,
        description="Small model to use for tasks like title generation in the format of provider/model",
    )
    default_agent: str | None = Field(
        None,
        description="Default agent to use when none is specified. Must be a primary agent. Falls back to 'build' if not set or if the specified agent is invalid.",
    )
    username: str | None = Field(
        None,
        description="Custom username to display in conversations instead of system username",
    )
    mode: dict[str, Agent] | None = Field(
        None,
        description="@deprecated Use `agent` field instead.",
    )
    agent: dict[str, Agent] | None = Field(
        None,
        description="Agent configuration, see https://opencode.ai/docs/agents",
    )
    provider: dict[str, Provider] | None = Field(
        None,
        description="Custom provider configurations and model overrides",
    )
    mcp: dict[str, McpLocal | McpRemote | dict[str, bool]] | None = Field(
        None,
        description="MCP (Model Context Protocol) server configurations",
    )
    formatter: dict[str, Any] | Literal[False] | None = None
    lsp: dict[str, Any] | Literal[False] | None = None
    instructions: list[str] | None = Field(
        None,
        description="Additional instruction files or patterns to include",
    )
    layout: str | None = Field(None, description="@deprecated Always uses stretch layout.")
    permission: dict[str, Any] | None = None
    tools: dict[str, bool] | None = None
    enterprise: dict[str, Any] | None = None
    compaction: Compaction | None = None
    experimental: Experimental | None = None

    class Config:
        extra = "forbid"
        populate_by_name = True


class Config:
    """Main configuration manager."""

    Info = ConfigInfo
    Command = Command
    Agent = Agent
    Skills = Skills
    Server = Server
    Provider = Provider
    McpLocal = McpLocal
    McpRemote = McpRemote
    Compaction = Compaction
    Experimental = Experimental

    _state: dict[str, Any] | None = None

    @staticmethod
    def managed_config_dir() -> str:
        """Get managed configuration directory for enterprise deployments.

        Returns:
            Path to managed config directory
        """
        if "OPENCODE_TEST_MANAGED_CONFIG_DIR" in os.environ:
            return os.environ["OPENCODE_TEST_MANAGED_CONFIG_DIR"]

        if sys.platform == "darwin":
            return "/Library/Application Support/opencode"
        elif sys.platform == "win32":
            program_data = os.environ.get("ProgramData", "C:\\ProgramData")
            return str(Path(program_data) / "opencode")
        else:
            return "/etc/opencode"

    @staticmethod
    def _merge_config_concat_arrays(target: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
        """Merge configs, concatenating array fields instead of replacing them.

        Args:
            target: Target configuration
            source: Source configuration to merge

        Returns:
            Merged configuration
        """
        merged = merge_deep(target, source)

        # Concatenate plugin arrays
        if target.get("plugin") and source.get("plugin"):
            merged["plugin"] = list(set(target["plugin"] + source["plugin"]))

        # Concatenate instructions arrays
        if target.get("instructions") and source.get("instructions"):
            merged["instructions"] = list(set(target["instructions"] + source["instructions"]))

        return merged

    @classmethod
    async def _load_file(cls, filepath: str) -> dict[str, Any]:
        """Load configuration from a file.

        Args:
            filepath: Path to config file

        Returns:
            Parsed configuration dictionary
        """
        log.info("loading", path=filepath)
        text = await ConfigPaths.read_file(filepath)
        if not text:
            return {}
        return await cls._load(text, filepath)

    @classmethod
    async def _load(cls, text: str, filepath: str) -> dict[str, Any]:
        """Parse and validate configuration text.

        Args:
            text: Configuration text
            filepath: Path to config file

        Returns:
            Validated configuration dictionary
        """
        data = await ConfigPaths.parse_text(text, filepath)

        # Remove deprecated TUI keys
        if isinstance(data, dict):
            normalized = dict(data)
            had_legacy = "theme" in normalized or "keybinds" in normalized or "tui" in normalized
            if had_legacy:
                normalized.pop("theme", None)
                normalized.pop("keybinds", None)
                normalized.pop("tui", None)
                log.warn("tui keys in opencode config are deprecated; move them to tui.json", path=filepath)
            data = normalized

        try:
            parsed = ConfigInfo.model_validate(data)
            result = parsed.model_dump(exclude_none=True, by_alias=True)

            # Add schema if missing
            if "$schema" not in result and await anyio.Path(filepath).is_file():
                result["$schema"] = "https://opencode.ai/config.json"
                # Try to update file with schema
                try:
                    updated = text.replace("{", '{\n  "$schema": "https://opencode.ai/config.json",', 1)
                    await Filesystem.write(filepath, updated)
                except Exception as e:
                    log.debug("failed to add schema to config file", path=filepath, error=e)

            return result
        except Exception as error:
            raise ConfigPaths.InvalidError(
                path=filepath,
                message=str(error),
            ) from error

    @classmethod
    async def get_global(cls) -> dict[str, Any]:
        """Get global configuration.

        Returns:
            Global configuration dictionary
        """
        result: dict[str, Any] = {}

        # Load from various global config files
        config_dir = Global.Path.config
        for filename in ["config.json", "opencode.json"]:
            filepath = str(Path(config_dir) / filename)
            config = await cls._load_file(filepath)
            result = merge_deep(result, config)

        return result

    @classmethod
    async def get(cls) -> dict[str, Any]:
        """Get complete configuration with all precedence rules applied.

        Returns:
            Complete configuration dictionary
        """
        if cls._state is not None:
            return cls._state

        result: dict[str, Any] = {}

        # 1. Global config
        result = cls._merge_config_concat_arrays(result, await cls.get_global())

        # 2. Custom config path
        if Flag.OPENCODE_CONFIG:
            result = cls._merge_config_concat_arrays(result, await cls._load_file(Flag.OPENCODE_CONFIG))
            log.debug("loaded custom config", path=Flag.OPENCODE_CONFIG)

        # 3. Project config (simplified - full implementation would use Instance)
        # if not Flag.OPENCODE_DISABLE_PROJECT_CONFIG:
        #     for file in await ConfigPaths.project_files("opencode", directory, worktree):
        #         result = cls._merge_config_concat_arrays(result, await cls._load_file(file))

        # Initialize nested structures
        result.setdefault("agent", {})
        result.setdefault("mode", {})
        result.setdefault("plugin", [])

        # 4. Inline config content
        if "OPENCODE_CONFIG_CONTENT" in os.environ:
            inline = await cls._load(
                os.environ["OPENCODE_CONFIG_CONTENT"],
                "OPENCODE_CONFIG_CONTENT",
            )
            result = cls._merge_config_concat_arrays(result, inline)
            log.debug("loaded custom config from OPENCODE_CONFIG_CONTENT")

        # 5. Managed config (highest priority)
        managed_dir = cls.managed_config_dir()
        if await anyio.Path(managed_dir).exists():
            filepath = str(Path(managed_dir) / "opencode.json")
            result = cls._merge_config_concat_arrays(result, await cls._load_file(filepath))

        # Migrate deprecated mode field to agent field
        for name, mode_config in (result.get("mode") or {}).items():
            if isinstance(mode_config, dict):
                agent_config = dict(mode_config)
                agent_config["mode"] = "primary"
                result["agent"][name] = agent_config

        # Handle permission flag override
        if Flag.OPENCODE_PERMISSION:
            import json

            result["permission"] = merge_deep(
                result.get("permission", {}),
                json.loads(Flag.OPENCODE_PERMISSION),
            )

        # Backwards compatibility: legacy top-level `tools` config
        if result.get("tools"):
            perms: dict[str, str] = {}
            for tool, enabled in result["tools"].items():
                action = "allow" if enabled else "deny"
                if tool in ("write", "edit", "patch", "multiedit"):
                    perms["edit"] = action
                else:
                    perms[tool] = action
            result["permission"] = merge_deep(perms, result.get("permission", {}))

        # Set default username
        if not result.get("username"):
            result["username"] = getpass.getuser()

        # Handle migration from autoshare to share field
        if result.get("autoshare") is True and not result.get("share"):
            result["share"] = "auto"

        # Apply flag overrides for compaction settings
        if Flag.OPENCODE_DISABLE_AUTOCOMPACT:
            if "compaction" not in result:
                result["compaction"] = {}
            result["compaction"]["auto"] = False

        if Flag.OPENCODE_DISABLE_PRUNE:
            if "compaction" not in result:
                result["compaction"] = {}
            result["compaction"]["prune"] = False

        # Deduplicate plugins
        if result.get("plugin"):
            result["plugin"] = cls._deduplicate_plugins(result["plugin"])

        cls._state = result
        return result

    @staticmethod
    def _get_plugin_name(plugin: str) -> str:
        """Extract canonical plugin name from plugin specifier.

        Args:
            plugin: Plugin specifier (file:// URL or npm package)

        Returns:
            Canonical plugin name
        """
        if plugin.startswith("file://"):
            return Path(plugin.replace("file://", "")).stem

        last_at = plugin.rfind("@")
        if last_at > 0:
            return plugin[:last_at]

        return plugin

    @classmethod
    def _deduplicate_plugins(cls, plugins: list[str]) -> list[str]:
        """Deduplicate plugins by name, with later entries (higher priority) winning.

        Args:
            plugins: List of plugin specifiers

        Returns:
            Deduplicated list of plugin specifiers
        """
        seen_names: set[str] = set()
        unique_specifiers: list[str] = []

        for specifier in reversed(plugins):
            name = cls._get_plugin_name(specifier)
            if name not in seen_names:
                seen_names.add(name)
                unique_specifiers.append(specifier)

        return list(reversed(unique_specifiers))

    @classmethod
    def reset(cls) -> None:
        """Reset cached state."""
        cls._state = None
