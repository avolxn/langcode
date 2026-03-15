"""Named error utilities."""

from typing import Any


class NamedError(Exception):
    """Base class for named errors with structured data."""

    def __init__(self, name: str, data: dict[str, Any]):
        """Initialize named error.

        Args:
            name: Error name/type
            data: Error data dictionary
        """
        self.name = name
        self.data = data
        message = data.get("message", name)
        super().__init__(message)

    def to_object(self) -> dict[str, Any]:
        """Convert error to dictionary representation.

        Returns:
            Dictionary with error name and data
        """
        return {
            "name": self.name,
            "data": self.data,
        }


class NotFoundError(NamedError):
    """Resource not found in storage."""

    def __init__(self, message: str):
        super().__init__(
            name="StorageNotFoundError",
            data={"message": message},
        )


class FrontmatterError(NamedError):
    """Error parsing frontmatter in configuration file."""

    def __init__(self, path: str, message: str):
        super().__init__(
            name="ConfigFrontmatterError",
            data={"path": path, "message": message},
        )


class JsonError(NamedError):
    """Error parsing JSON configuration file."""

    def __init__(self, path: str, message: str | None = None):
        super().__init__(
            name="ConfigJsonError",
            data={"path": path, "message": message},
        )


class InvalidError(NamedError):
    """Invalid configuration error."""

    def __init__(self, path: str, message: str | None = None, issues: Any = None):
        super().__init__(
            name="ConfigInvalidError",
            data={"path": path, "message": message, "issues": issues},
        )
