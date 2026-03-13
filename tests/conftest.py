"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def temp_dir(tmp_path):
    """Provide a temporary directory for tests."""
    return tmp_path


@pytest.fixture
def mock_config():
    """Provide a mock configuration for tests."""
    return {
        "providers": {},
        "mcp": {"servers": {}},
        "plugins": [],
        "skills": {"paths": [], "urls": []},
    }
