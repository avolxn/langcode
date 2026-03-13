"""Pytest configuration and fixtures."""

from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Provide a temporary directory for tests."""
    return tmp_path


@pytest.fixture
def mock_config() -> dict[str, Any]:
    """Provide a mock configuration for tests."""
    return {
        "providers": {},
        "mcp": {"servers": {}},
        "plugins": [],
        "skills": {"paths": [], "urls": []},
    }
