"""Configuration markdown file parsing utilities."""

import re
from typing import Any

import frontmatter

from langcode.util.error import NamedError
from langcode.util.filesystem import Filesystem


class ConfigMarkdown:
    """Utilities for parsing markdown configuration files with frontmatter."""

    FILE_REGEX = re.compile(r"(?<![\w`])@(\.?[^\s`,.]*(?:\.[^\s`,.]+)*)")
    SHELL_REGEX = re.compile(r"!`([^`]+)`")

    @classmethod
    def files(cls, template: str) -> list[re.Match[str]]:
        """Extract file references from template string.

        Args:
            template: Template string to search

        Returns:
            List of regex matches for file references
        """
        return list(cls.FILE_REGEX.finditer(template))

    @classmethod
    def shell(cls, template: str) -> list[re.Match[str]]:
        """Extract shell command references from template string.

        Args:
            template: Template string to search

        Returns:
            List of regex matches for shell commands
        """
        return list(cls.SHELL_REGEX.finditer(template))

    @classmethod
    def fallback_sanitization(cls, content: str) -> str:
        """Sanitize invalid YAML frontmatter for permissive parsing.

        Other coding agents like claude code allow invalid yaml in their
        frontmatter, we need to fallback to a more permissive parser for those cases.

        Args:
            content: Markdown content with frontmatter

        Returns:
            Sanitized content
        """
        match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---", content)
        if not match:
            return content

        frontmatter_text = match.group(1)
        lines = frontmatter_text.split("\n")
        result: list[str] = []

        for line in lines:
            # skip comments and empty lines
            if line.strip().startswith("#") or line.strip() == "":
                result.append(line)
                continue

            # skip lines that are continuations (indented)
            if re.match(r"^\s+", line):
                result.append(line)
                continue

            # match key: value pattern
            kv_match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*)$", line)
            if not kv_match:
                result.append(line)
                continue

            key = kv_match.group(1)
            value = kv_match.group(2).strip()

            # skip if value is empty, already quoted, or uses block scalar
            if value == "" or value == ">" or value == "|" or value.startswith('"') or value.startswith("'"):
                result.append(line)
                continue

            # if value contains a colon, convert to block scalar
            if ":" in value:
                result.append(f"{key}: |-")
                result.append(f"  {value}")
                continue

            result.append(line)

        processed = "\n".join(result)
        return content.replace(frontmatter_text, processed, 1)

    @classmethod
    async def parse(cls, file_path: str) -> Any:
        """Parse markdown file with YAML frontmatter.

        Args:
            file_path: Path to markdown file

        Returns:
            Parsed frontmatter and content

        Raises:
            FrontmatterError: If parsing fails
        """
        template = await Filesystem.read(file_path)

        try:
            md = frontmatter.loads(template)
            return md
        except Exception:
            try:
                return frontmatter.loads(cls.fallback_sanitization(template))
            except Exception as err:
                raise FrontmatterError(
                    path=file_path,
                    message=f"{file_path}: Failed to parse YAML frontmatter: {err}",
                ) from err


class FrontmatterError(NamedError):
    """Error parsing frontmatter in configuration file."""

    def __init__(self, path: str, message: str):
        super().__init__(
            name="ConfigFrontmatterError",
            data={"path": path, "message": message},
        )


ConfigMarkdown.FrontmatterError = FrontmatterError
