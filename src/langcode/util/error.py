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

    @classmethod
    def is_instance(cls, obj: Any) -> bool:
        """Check if object is an instance of this error type.

        Args:
            obj: Object to check

        Returns:
            True if object is an instance of this error type
        """
        return isinstance(obj, cls)


class UnknownError(NamedError):
    """Unknown error type."""

    def __init__(self, data: dict[str, Any]):
        super().__init__("UnknownError", data)
