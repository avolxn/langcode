"""Unit tests for storage.storage module."""

import os
import json
import pytest
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock

from langcode.storage.storage import Storage, NotFoundError


@pytest.fixture
def temp_storage_dir(tmp_path):
    """Create a temporary storage directory."""
    storage_dir = tmp_path / "storage"
    storage_dir.mkdir()
    yield str(storage_dir)


@pytest.fixture
def mock_global_path(tmp_path):
    """Mock Global.Path.data."""
    with patch("langcode.global_config.Global") as mock_global:
        mock_global.Path.data = str(tmp_path)
        yield mock_global


class TestStorage:
    """Tests for Storage class."""

    @pytest.mark.asyncio
    async def test_write_and_read(self, mock_global_path, tmp_path):
        """Test writing and reading data."""
        # Reset state
        Storage._state = None

        # Create storage directory
        storage_dir = tmp_path / "storage"
        storage_dir.mkdir()

        # Write migration file to skip migrations
        (storage_dir / "migration").write_text("2")

        test_data = {"id": "test123", "name": "Test Item"}

        await Storage.write(["test", "item"], test_data)
        result = await Storage.read(["test", "item"])

        assert result == test_data

    @pytest.mark.asyncio
    async def test_read_not_found(self, mock_global_path, tmp_path):
        """Test reading non-existent data raises NotFoundError."""
        Storage._state = None

        storage_dir = tmp_path / "storage"
        storage_dir.mkdir()
        (storage_dir / "migration").write_text("2")

        with pytest.raises(NotFoundError):
            await Storage.read(["nonexistent", "item"])

    @pytest.mark.asyncio
    async def test_update(self, mock_global_path, tmp_path):
        """Test updating data."""
        Storage._state = None

        storage_dir = tmp_path / "storage"
        storage_dir.mkdir()
        (storage_dir / "migration").write_text("2")

        initial_data = {"id": "test123", "count": 0}
        await Storage.write(["test", "item"], initial_data)

        def increment(data):
            data["count"] += 1

        result = await Storage.update(["test", "item"], increment)

        assert result["count"] == 1

        # Verify it was persisted
        read_result = await Storage.read(["test", "item"])
        assert read_result["count"] == 1

    @pytest.mark.asyncio
    async def test_remove(self, mock_global_path, tmp_path):
        """Test removing data."""
        Storage._state = None

        storage_dir = tmp_path / "storage"
        storage_dir.mkdir()
        (storage_dir / "migration").write_text("2")

        test_data = {"id": "test123"}
        await Storage.write(["test", "item"], test_data)

        # Verify it exists
        result = await Storage.read(["test", "item"])
        assert result == test_data

        # Remove it
        await Storage.remove(["test", "item"])

        # Verify it's gone
        with pytest.raises(NotFoundError):
            await Storage.read(["test", "item"])

    @pytest.mark.asyncio
    async def test_list(self, mock_global_path, tmp_path):
        """Test listing storage entries."""
        Storage._state = None

        storage_dir = tmp_path / "storage"
        storage_dir.mkdir()
        (storage_dir / "migration").write_text("2")

        # Write multiple items
        await Storage.write(["test", "item1"], {"id": "1"})
        await Storage.write(["test", "item2"], {"id": "2"})
        await Storage.write(["test", "nested", "item3"], {"id": "3"})

        # List items with prefix
        results = await Storage.list(["test"])

        assert len(results) >= 2
        assert ["test", "item1"] in results
        assert ["test", "item2"] in results

    @pytest.mark.asyncio
    async def test_list_empty_prefix(self, mock_global_path, tmp_path):
        """Test listing with non-existent prefix returns empty list."""
        Storage._state = None

        storage_dir = tmp_path / "storage"
        storage_dir.mkdir()
        (storage_dir / "migration").write_text("2")

        results = await Storage.list(["nonexistent"])
        assert results == []

    @pytest.mark.asyncio
    async def test_not_found_error(self):
        """Test NotFoundError exception."""
        error = NotFoundError("test message")
        assert error.message == "test message"
        assert str(error) == "test message"


class TestStorageMigrations:
    """Tests for storage migrations."""

    @pytest.mark.asyncio
    async def test_storage_initialization(self, mock_global_path, tmp_path):
        """Test that storage initializes correctly."""
        Storage._state = None

        storage_dir = tmp_path / "storage"
        storage_dir.mkdir()

        # First call should initialize state
        state1 = await Storage._get_state()
        assert state1 is not None
        assert "dir" in state1

        # Second call should reuse cached state
        state2 = await Storage._get_state()
        assert state2 is state1  # Same object
