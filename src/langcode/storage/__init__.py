"""Storage module for LangCode.

Provides JSON file storage for all data.
"""

from .storage import NotFoundError, Storage

__all__ = ["Storage", "NotFoundError"]
