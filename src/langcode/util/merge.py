"""Deep merge utility for dictionaries."""

from typing import Any


def merge_deep(target: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    """Deep merge two dictionaries.

    Args:
        target: Target dictionary
        source: Source dictionary to merge into target

    Returns:
        Merged dictionary (new instance)
    """
    result = dict(target)

    for key, value in source.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_deep(result[key], value)
        else:
            result[key] = value

    return result
