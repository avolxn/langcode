"""Unit tests for utility modules."""

import os
import pytest
from pathlib import Path

from langcode.util.lazy import Lazy, lazy
from langcode.util.log import Log


class TestLazy:
    """Tests for Lazy class."""

    def test_lazy_initialization(self):
        """Test lazy initialization."""
        call_count = [0]

        def initializer():
            call_count[0] += 1
            return "initialized"

        lazy_value = Lazy(initializer)

        # Should not be initialized yet
        assert call_count[0] == 0

        # First call should initialize
        result1 = lazy_value()
        assert result1 == "initialized"
        assert call_count[0] == 1

        # Second call should reuse value
        result2 = lazy_value()
        assert result2 == "initialized"
        assert call_count[0] == 1

    def test_lazy_reset(self):
        """Test lazy reset."""
        call_count = [0]

        def initializer():
            call_count[0] += 1
            return call_count[0]

        lazy_value = Lazy(initializer)

        # Initialize
        result1 = lazy_value()
        assert result1 == 1

        # Reset
        lazy_value.reset()

        # Should initialize again
        result2 = lazy_value()
        assert result2 == 2

    @pytest.mark.asyncio
    async def test_lazy_decorator(self):
        """Test lazy decorator for async functions."""
        call_count = [0]

        @lazy
        async def async_initializer():
            call_count[0] += 1
            return "async_initialized"

        # First call
        result1 = await async_initializer()
        assert result1 == "async_initialized"
        assert call_count[0] == 1

        # Second call should reuse
        result2 = await async_initializer()
        assert result2 == "async_initialized"
        assert call_count[0] == 1


class TestLog:
    """Tests for Log class."""

    def test_create_logger(self):
        """Test creating a logger."""
        log = Log.create(service="test")
        assert log is not None

    def test_log_methods(self, caplog):
        """Test logging methods."""
        import logging

        caplog.set_level(logging.INFO)

        log = Log.create(service="test")

        log.info("info message", key="value")
        log.warn("warn message")
        log.error("error message", error="details")
        log.debug("debug message")

        # Check that messages were logged
        assert any("info message" in record.message for record in caplog.records)


class TestGlob:
    """Tests for Glob utilities."""

    @pytest.mark.asyncio
    async def test_glob_scan(self, tmp_path):
        """Test glob scanning."""
        from langcode.util.glob import Glob

        # Create test files
        (tmp_path / "file1.txt").write_text("test")
        (tmp_path / "file2.txt").write_text("test")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "file3.txt").write_text("test")

        # Scan for all txt files
        results = await Glob.scan("*.txt", cwd=str(tmp_path))
        assert len(results) == 2

        # Scan recursively
        results = await Glob.scan("**/*.txt", cwd=str(tmp_path))
        assert len(results) == 3

    @pytest.mark.asyncio
    async def test_glob_filter_by_type(self, tmp_path):
        """Test glob filtering by type."""
        from langcode.util.glob import Glob

        # Create test files and directories
        (tmp_path / "file.txt").write_text("test")
        (tmp_path / "dir").mkdir()

        # Filter files only
        results = await Glob.scan("*", cwd=str(tmp_path), include="file")
        assert len(results) == 1
        assert "file.txt" in results

        # Filter directories only
        results = await Glob.scan("*", cwd=str(tmp_path), include="dir")
        assert len(results) == 1
        assert "dir" in results


class TestFilesystem:
    """Tests for Filesystem utilities."""

    @pytest.mark.asyncio
    async def test_read_write_json(self, tmp_path):
        """Test reading and writing JSON."""
        from langcode.util.filesystem import Filesystem

        test_file = tmp_path / "test.json"
        test_data = {"key": "value", "number": 42}

        await Filesystem.write_json(str(test_file), test_data)
        result = await Filesystem.read_json(str(test_file))

        assert result == test_data

    @pytest.mark.asyncio
    async def test_read_write_text(self, tmp_path):
        """Test reading and writing text."""
        from langcode.util.filesystem import Filesystem

        test_file = tmp_path / "test.txt"
        test_content = "Hello, World!"

        await Filesystem.write(str(test_file), test_content)
        result = await Filesystem.read(str(test_file))

        assert result == test_content

    @pytest.mark.asyncio
    async def test_is_dir(self, tmp_path):
        """Test directory check."""
        from langcode.util.filesystem import Filesystem

        # Create directory
        test_dir = tmp_path / "testdir"
        test_dir.mkdir()

        assert await Filesystem.is_dir(str(test_dir)) is True
        assert await Filesystem.is_dir(str(tmp_path / "nonexistent")) is False


class TestLock:
    """Tests for Lock utilities."""

    @pytest.mark.asyncio
    async def test_read_lock(self, tmp_path):
        """Test read lock."""
        from langcode.util.lock import Lock

        lock_file = tmp_path / "test.lock"

        # Lock should work without errors
        async with Lock.read(str(lock_file)):
            pass  # Lock acquired successfully

    @pytest.mark.asyncio
    async def test_write_lock(self, tmp_path):
        """Test write lock."""
        from langcode.util.lock import Lock

        lock_file = tmp_path / "test.lock"

        # Lock should work without errors
        async with Lock.write(str(lock_file)):
            pass  # Lock acquired successfully
