"""Configuration path utilities."""

import json
import os
import re
from pathlib import Path
from typing import Any, Literal

from langcode.config.flag import Flag
from langcode.config.globals import Global
from langcode.util.error import InvalidError, JsonError
from langcode.util.filesystem import Filesystem


class ConfigPaths:
    """Utilities for finding and parsing configuration files."""

    @staticmethod
    async def project_files(name: str, directory: str, worktree: str) -> list[str]:
        """Find project configuration files by searching up the directory tree.

        Args:
            name: Base name of config file (e.g., 'opencode', 'tui')
            directory: Starting directory
            worktree: Worktree root directory

        Returns:
            List of configuration file paths in order (root to leaf)
        """
        files: list[str] = []
        found = await Filesystem.find_up(f"{name}.json", directory, worktree)
        for resolved in reversed(found):
            files.append(resolved)
        return files

    @staticmethod
    async def directories(directory: str, worktree: str) -> list[str]:
        """Get all configuration directories in precedence order.

        Args:
            directory: Current working directory
            worktree: Worktree root directory

        Returns:
            List of configuration directories
        """
        dirs = [Global.Path.config]

        if not Flag.OPENCODE_DISABLE_PROJECT_CONFIG:
            async for path in Filesystem.up(
                targets=[".opencode"],
                start=directory,
                stop=worktree,
            ):
                dirs.append(path)

        async for path in Filesystem.up(
            targets=[".opencode"],
            start=Global.Path.home,
            stop=Global.Path.home,
        ):
            dirs.append(path)

        if Flag.OPENCODE_CONFIG_DIR:
            dirs.append(Flag.OPENCODE_CONFIG_DIR)

        return dirs

    @staticmethod
    def file_in_directory(dir_path: str, name: str) -> list[str]:
        """Get potential config file paths in a directory.

        Args:
            dir_path: Directory path
            name: Base name of config file

        Returns:
            List of potential file paths
        """
        base = Path(dir_path)
        return [str(base / f"{name}.json")]

    @staticmethod
    async def read_file(filepath: str) -> str | None:
        """Read a config file, returning None for missing files.

        Args:
            filepath: Path to config file

        Returns:
            File contents or None if file doesn't exist

        Raises:
            JsonError: For read errors other than file not found
        """
        try:
            return await Filesystem.read(filepath)
        except FileNotFoundError:
            return None
        except Exception as err:
            raise JsonError(path=filepath) from err

    @staticmethod
    async def substitute(
        text: str,
        input_source: str | dict[str, str],
        missing: Literal["error", "empty"] = "error",
    ) -> str:
        """Apply {env:VAR} and {file:path} substitutions to config text.

        Args:
            text: Configuration text
            input_source: Either a file path string or dict with 'source' and 'dir' keys
            missing: How to handle missing files ('error' or 'empty')

        Returns:
            Text with substitutions applied

        Raises:
            InvalidError: If file reference is invalid or missing
        """

        # Apply environment variable substitutions
        def env_replacer(match: Any) -> str:
            var_name = match.group(1)
            return os.environ.get(var_name, "")

        text = re.sub(r"\{env:([^}]+)\}", env_replacer, text)

        # Apply file substitutions
        file_matches = list(re.finditer(r"\{file:[^}]+\}", text))
        if not file_matches:
            return text

        if isinstance(input_source, str):
            config_dir = str(Path(input_source).parent)
            config_source = input_source
        else:
            config_dir = input_source["dir"]
            config_source = input_source["source"]

        out = ""
        cursor = 0

        for match in file_matches:
            token = match.group(0)
            index = match.start()
            out += text[cursor:index]

            # Extract file path
            file_path = token.replace("{file:", "").replace("}", "")
            if file_path.startswith("~/"):
                file_path = str(Path.home() / file_path[2:])

            resolved_path = file_path if Path(file_path).is_absolute() else str(Path(config_dir) / file_path)

            try:
                file_content = (await Filesystem.read(resolved_path)).strip()
            except FileNotFoundError as error:
                if missing == "empty":
                    file_content = ""
                else:
                    raise InvalidError(
                        path=config_source,
                        message=f'bad file reference: "{token}" {resolved_path} does not exist',
                    ) from error
            except Exception as error:
                raise InvalidError(
                    path=config_source,
                    message=f'bad file reference: "{token}"',
                ) from error

            # Escape the content for JSON string
            out += json.dumps(file_content)[1:-1]
            cursor = index + len(token)

        out += text[cursor:]
        return out

    @staticmethod
    async def parse_text(
        text: str,
        input_source: str | dict[str, str],
        missing: Literal["error", "empty"] = "error",
    ) -> Any:
        """Substitute and parse JSON text.

        Args:
            text: JSON text to parse
            input_source: Either a file path string or dict with 'source' and 'dir' keys
            missing: How to handle missing file references

        Returns:
            Parsed JSON data

        Raises:
            JsonError: On syntax errors
        """
        config_source = input_source if isinstance(input_source, str) else input_source["source"]
        text = await ConfigPaths.substitute(text, input_source, missing)

        try:
            data = json.loads(text)
            return data
        except Exception as e:
            raise JsonError(
                path=config_source,
                message=f"\n--- JSON Input ---\n{text}\n--- Errors ---\n{str(e)}\n--- End ---",
            ) from e
