"""Lazy initialization utilities."""

from collections.abc import Awaitable, Callable, Coroutine
from typing import Any, Generic, TypeVar, cast

T = TypeVar("T")


class Lazy(Generic[T]):
    """Lazy initialization wrapper.

    Defers initialization until first access and caches the result.

    Attributes:
        _initializer: Function to call for initialization
        _value: Cached initialized value
        _initialized: Whether initialization has occurred
    """

    def __init__(self, initializer: Callable[[], T]):
        self._initializer = initializer
        self._value: T | None = None
        self._initialized = False

    def __call__(self) -> T:
        """Get or initialize the value.

        Returns:
            The initialized value
        """
        if not self._initialized:
            self._value = self._initializer()
            self._initialized = True
        return cast(T, self._value)

    def reset(self):
        """Reset the lazy value."""
        self._value = None
        self._initialized = False


def lazy(func: Callable[[], Awaitable[T]]) -> Callable[[], Coroutine[Any, Any, T]]:
    """Decorator for lazy initialization of async functions.

    Args:
        func: Async function to wrap with lazy initialization

    Returns:
        Wrapped function that caches the result
    """
    _value: T | None = None
    _initialized = False

    async def wrapper() -> T:
        nonlocal _value, _initialized
        if not _initialized:
            _value = await func()
            _initialized = True
        return cast(T, _value)

    return wrapper
