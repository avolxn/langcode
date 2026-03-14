"""Feature flags."""

import os


def _truthy(key: str) -> bool:
    """Check if environment variable is truthy."""
    value = os.environ.get(key, "").lower()
    return value in ("true", "1")


def _falsy(key: str) -> bool:
    """Check if environment variable is falsy."""
    value = os.environ.get(key, "").lower()
    return value in ("false", "0")


class Flag:
    """Feature flags for LangCode.

    Matches OpenCode's flag system for environment-based configuration.
    """

    # Storage flags
    OPENCODE_DISABLE_CHANNEL_DB: bool = False
    OPENCODE_SKIP_MIGRATIONS: bool = False

    # Configuration flags
    OPENCODE_CONFIG: str | None = os.environ.get("OPENCODE_CONFIG")
    OPENCODE_TUI_CONFIG: str | None = os.environ.get("OPENCODE_TUI_CONFIG")
    OPENCODE_CONFIG_DIR: str | None = os.environ.get("OPENCODE_CONFIG_DIR")
    OPENCODE_CONFIG_CONTENT: str | None = os.environ.get("OPENCODE_CONFIG_CONTENT")
    OPENCODE_DISABLE_PROJECT_CONFIG: bool = _truthy("OPENCODE_DISABLE_PROJECT_CONFIG")

    # Permission flags
    OPENCODE_PERMISSION: str | None = os.environ.get("OPENCODE_PERMISSION")

    # Compaction flags
    OPENCODE_DISABLE_AUTOCOMPACT: bool = _truthy("OPENCODE_DISABLE_AUTOCOMPACT")
    OPENCODE_DISABLE_PRUNE: bool = _truthy("OPENCODE_DISABLE_PRUNE")

    # Feature flags
    OPENCODE_AUTO_SHARE: bool = _truthy("OPENCODE_AUTO_SHARE")
    OPENCODE_DISABLE_AUTOUPDATE: bool = _truthy("OPENCODE_DISABLE_AUTOUPDATE")
    OPENCODE_DISABLE_TERMINAL_TITLE: bool = _truthy("OPENCODE_DISABLE_TERMINAL_TITLE")
    OPENCODE_DISABLE_DEFAULT_PLUGINS: bool = _truthy("OPENCODE_DISABLE_DEFAULT_PLUGINS")
    OPENCODE_DISABLE_LSP_DOWNLOAD: bool = _truthy("OPENCODE_DISABLE_LSP_DOWNLOAD")
    OPENCODE_ENABLE_EXPERIMENTAL_MODELS: bool = _truthy("OPENCODE_ENABLE_EXPERIMENTAL_MODELS")
    OPENCODE_DISABLE_MODELS_FETCH: bool = _truthy("OPENCODE_DISABLE_MODELS_FETCH")
    OPENCODE_ENABLE_QUESTION_TOOL: bool = _truthy("OPENCODE_ENABLE_QUESTION_TOOL")

    # Claude Code flags
    OPENCODE_DISABLE_CLAUDE_CODE: bool = _truthy("OPENCODE_DISABLE_CLAUDE_CODE")
    OPENCODE_DISABLE_CLAUDE_CODE_PROMPT: bool = _truthy("OPENCODE_DISABLE_CLAUDE_CODE") or _truthy(
        "OPENCODE_DISABLE_CLAUDE_CODE_PROMPT"
    )
    OPENCODE_DISABLE_CLAUDE_CODE_SKILLS: bool = _truthy("OPENCODE_DISABLE_CLAUDE_CODE") or _truthy(
        "OPENCODE_DISABLE_CLAUDE_CODE_SKILLS"
    )
    OPENCODE_DISABLE_EXTERNAL_SKILLS: bool = _truthy("OPENCODE_DISABLE_CLAUDE_CODE_SKILLS") or _truthy(
        "OPENCODE_DISABLE_EXTERNAL_SKILLS"
    )

    # Server flags
    OPENCODE_SERVER_PASSWORD: str | None = os.environ.get("OPENCODE_SERVER_PASSWORD")
    OPENCODE_SERVER_USERNAME: str | None = os.environ.get("OPENCODE_SERVER_USERNAME")

    # Development/testing flags
    OPENCODE_FAKE_VCS: str | None = os.environ.get("OPENCODE_FAKE_VCS")
    OPENCODE_CLIENT: str | None = os.environ.get("OPENCODE_CLIENT")

    # Experimental flags
    OPENCODE_EXPERIMENTAL: bool = _truthy("OPENCODE_EXPERIMENTAL")
    OPENCODE_EXPERIMENTAL_FILEWATCHER: bool = _truthy("OPENCODE_EXPERIMENTAL_FILEWATCHER")
    OPENCODE_EXPERIMENTAL_DISABLE_FILEWATCHER: bool = _truthy("OPENCODE_EXPERIMENTAL_DISABLE_FILEWATCHER")
    OPENCODE_EXPERIMENTAL_ICON_DISCOVERY: bool = _truthy("OPENCODE_EXPERIMENTAL") or _truthy(
        "OPENCODE_EXPERIMENTAL_ICON_DISCOVERY"
    )

    # Platform-specific defaults
    OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT: bool = (
        _truthy("OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT")
        if "OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT" in os.environ
        else os.name == "nt"  # Default to True on Windows
    )

    # Git bash path (Windows)
    OPENCODE_GIT_BASH_PATH: str | None = os.environ.get("OPENCODE_GIT_BASH_PATH")
