"""Unit tests for configuration module."""

import os
import tempfile
from pathlib import Path

import pytest

from langcode.config.config import Config
from langcode.config.markdown import ConfigMarkdown
from langcode.config.paths import ConfigPaths
from langcode.util.merge import merge_deep


class TestConfigMarkdown:
    """Tests for ConfigMarkdown utilities."""

    def test_file_regex(self):
        """Test file reference extraction."""
        template = "Read @file.txt and @./relative/path.py"
        matches = ConfigMarkdown.files(template)
        assert len(matches) == 2
        assert matches[0].group(1) == "file.txt"
        assert matches[1].group(1) == "./relative/path.py"

    def test_shell_regex(self):
        """Test shell command extraction."""
        template = "Run !`echo hello` and !`ls -la`"
        matches = ConfigMarkdown.shell(template)
        assert len(matches) == 2
        assert matches[0].group(1) == "echo hello"
        assert matches[1].group(1) == "ls -la"

    def test_fallback_sanitization(self):
        """Test YAML frontmatter sanitization."""
        content = """---
key: value:with:colons
normal: value
---
Body content"""
        sanitized = ConfigMarkdown.fallback_sanitization(content)
        assert "key: |-" in sanitized
        assert "  value:with:colons" in sanitized
        assert "normal: value" in sanitized

    @pytest.mark.asyncio
    async def test_parse_valid_frontmatter(self):
        """Test parsing valid markdown with frontmatter."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("""---
title: Test
description: A test file
---
# Content
This is the body.""")
            f.flush()

            try:
                result = await ConfigMarkdown.parse(f.name)
                assert result.metadata["title"] == "Test"
                assert result.metadata["description"] == "A test file"
                assert "# Content" in result.content
            finally:
                os.unlink(f.name)


class TestConfigPaths:
    """Tests for ConfigPaths utilities."""

    def test_file_in_directory(self):
        """Test file path generation."""
        files = ConfigPaths.file_in_directory("/test/dir", "config")
        assert len(files) == 1
        assert files[0] == "/test/dir/config.json"

    @pytest.mark.asyncio
    async def test_read_file_missing(self):
        """Test reading non-existent file returns None."""
        result = await ConfigPaths.read_file("/nonexistent/file.json")
        assert result is None

    @pytest.mark.asyncio
    async def test_substitute_env_vars(self):
        """Test environment variable substitution."""
        os.environ["TEST_VAR"] = "test_value"
        text = "Config with {env:TEST_VAR}"
        result = await ConfigPaths.substitute(text, "/test/config.json")
        assert result == "Config with test_value"
        del os.environ["TEST_VAR"]

    @pytest.mark.asyncio
    async def test_substitute_file_reference(self):
        """Test file reference substitution."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file to reference
            ref_file = os.path.join(tmpdir, "ref.txt")
            with open(ref_file, "w") as f:
                f.write("referenced content")

            # Create config with file reference
            text = 'Config with {file:ref.txt}'
            result = await ConfigPaths.substitute(text, os.path.join(tmpdir, "config.json"))
            assert "referenced content" in result

    @pytest.mark.asyncio
    async def test_parse_text_valid_json(self):
        """Test parsing valid JSON text."""
        text = '{"key": "value", "number": 42}'
        result = await ConfigPaths.parse_text(text, "/test/config.json")
        assert result["key"] == "value"
        assert result["number"] == 42


class TestConfig:
    """Tests for Config management."""

    def test_managed_config_dir_darwin(self):
        """Test managed config directory on macOS."""
        import sys
        original_platform = sys.platform
        sys.platform = "darwin"
        try:
            result = Config.managed_config_dir()
            assert result == "/Library/Application Support/opencode"
        finally:
            sys.platform = original_platform

    def test_managed_config_dir_linux(self):
        """Test managed config directory on Linux."""
        import sys
        original_platform = sys.platform
        sys.platform = "linux"
        try:
            result = Config.managed_config_dir()
            assert result == "/etc/opencode"
        finally:
            sys.platform = original_platform

    def test_get_plugin_name_file_url(self):
        """Test extracting plugin name from file:// URL."""
        plugin = "file:///path/to/plugin/my-plugin.js"
        name = Config._get_plugin_name(plugin)
        assert name == "my-plugin"

    def test_get_plugin_name_npm_package(self):
        """Test extracting plugin name from npm package."""
        plugin = "oh-my-opencode@2.4.3"
        name = Config._get_plugin_name(plugin)
        assert name == "oh-my-opencode"

    def test_get_plugin_name_scoped_package(self):
        """Test extracting plugin name from scoped npm package."""
        plugin = "@scope/pkg@1.0.0"
        name = Config._get_plugin_name(plugin)
        assert name == "@scope/pkg"

    def test_deduplicate_plugins(self):
        """Test plugin deduplication with priority."""
        plugins = [
            "plugin-a@1.0.0",
            "plugin-b@1.0.0",
            "plugin-a@2.0.0",  # Higher priority (later)
            "plugin-c@1.0.0",
        ]
        result = Config._deduplicate_plugins(plugins)
        assert len(result) == 3
        assert "plugin-a@2.0.0" in result
        assert "plugin-a@1.0.0" not in result
        assert "plugin-b@1.0.0" in result
        assert "plugin-c@1.0.0" in result

    def test_merge_config_concat_arrays(self):
        """Test config merging with array concatenation."""
        target = {
            "plugin": ["plugin-a"],
            "instructions": ["inst-a"],
            "other": "value1",
        }
        source = {
            "plugin": ["plugin-b"],
            "instructions": ["inst-b"],
            "other": "value2",
        }
        result = Config._merge_config_concat_arrays(target, source)
        assert set(result["plugin"]) == {"plugin-a", "plugin-b"}
        assert set(result["instructions"]) == {"inst-a", "inst-b"}
        assert result["other"] == "value2"

    @pytest.mark.asyncio
    async def test_load_valid_config(self):
        """Test loading valid configuration."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write('{"model": "anthropic/claude-3", "username": "testuser"}')
            f.flush()

            try:
                result = await Config._load_file(f.name)
                assert result["model"] == "anthropic/claude-3"
                assert result["username"] == "testuser"
            finally:
                os.unlink(f.name)

    @pytest.mark.asyncio
    async def test_load_config_with_deprecated_tui_keys(self):
        """Test loading config with deprecated TUI keys."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write('{"model": "test", "theme": "dark", "keybinds": {}}')
            f.flush()

            try:
                result = await Config._load_file(f.name)
                assert result["model"] == "test"
                assert "theme" not in result
                assert "keybinds" not in result
            finally:
                os.unlink(f.name)


class TestMergeDeep:
    """Tests for deep merge utility."""

    def test_merge_simple_dicts(self):
        """Test merging simple dictionaries."""
        target = {"a": 1, "b": 2}
        source = {"b": 3, "c": 4}
        result = merge_deep(target, source)
        assert result == {"a": 1, "b": 3, "c": 4}

    def test_merge_nested_dicts(self):
        """Test merging nested dictionaries."""
        target = {"a": {"x": 1, "y": 2}, "b": 3}
        source = {"a": {"y": 3, "z": 4}, "c": 5}
        result = merge_deep(target, source)
        assert result == {"a": {"x": 1, "y": 3, "z": 4}, "b": 3, "c": 5}

    def test_merge_does_not_modify_original(self):
        """Test that merge creates new dict without modifying originals."""
        target = {"a": 1}
        source = {"b": 2}
        result = merge_deep(target, source)
        assert target == {"a": 1}
        assert source == {"b": 2}
        assert result == {"a": 1, "b": 2}

    def test_merge_with_non_dict_values(self):
        """Test merging when values are not dicts."""
        target = {"a": [1, 2], "b": "string"}
        source = {"a": [3, 4], "c": 123}
        result = merge_deep(target, source)
        assert result == {"a": [3, 4], "b": "string", "c": 123}
