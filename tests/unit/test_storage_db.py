"""Unit tests for storage.db module."""

import os
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from langcode.storage.db import Database, NotFoundError


@pytest.fixture
def temp_db_path(tmp_path):
    """Create a temporary database path."""
    db_path = tmp_path / "test.db"
    yield str(db_path)
    # Cleanup
    if db_path.exists():
        db_path.unlink()


@pytest.fixture
def mock_global_path(tmp_path):
    """Mock Global.Path.data."""
    with patch("langcode.global_config.Global") as mock_global:
        mock_global.Path.data = str(tmp_path)
        yield mock_global


class TestDatabase:
    """Tests for Database class."""

    def test_get_db_path_latest_channel(self, mock_global_path, tmp_path):
        """Test database path for latest channel."""
        with patch("langcode.installation.Installation") as mock_install:
            mock_install.CHANNEL = "latest"
            with patch("langcode.flag.flag.Flag") as mock_flag:
                mock_flag.OPENCODE_DISABLE_CHANNEL_DB = False
                path = Database._get_db_path()
                assert path == os.path.join(str(tmp_path), "opencode.db")

    def test_get_db_path_custom_channel(self, mock_global_path, tmp_path):
        """Test database path for custom channel."""
        with patch("langcode.installation.Installation") as mock_install:
            mock_install.CHANNEL = "dev-test"
            with patch("langcode.flag.flag.Flag") as mock_flag:
                mock_flag.OPENCODE_DISABLE_CHANNEL_DB = False
                path = Database._get_db_path()
                assert path == os.path.join(str(tmp_path), "opencode-dev-test.db")

    def test_get_db_path_sanitize_channel(self, mock_global_path, tmp_path):
        """Test database path sanitizes channel name."""
        with patch("langcode.installation.Installation") as mock_install:
            mock_install.CHANNEL = "test@#$channel"
            with patch("langcode.flag.flag.Flag") as mock_flag:
                mock_flag.OPENCODE_DISABLE_CHANNEL_DB = False
                path = Database._get_db_path()
                assert path == os.path.join(str(tmp_path), "opencode-test---channel.db")

    def test_parse_migration_timestamp(self):
        """Test parsing migration timestamp from directory name."""
        timestamp = Database._parse_migration_timestamp("20240315120000_init")
        assert timestamp > 0

        # Invalid format should return 0
        timestamp = Database._parse_migration_timestamp("invalid")
        assert timestamp == 0

    def test_close(self, mock_global_path):
        """Test database close."""
        # Reset lazy client first
        Database._client_lazy = None
        Database._engine = MagicMock()
        Database.close()
        assert Database._engine is None

    def test_not_found_error(self):
        """Test NotFoundError exception."""
        error = NotFoundError("test message")
        assert error.message == "test message"
        assert str(error) == "test message"


class TestDatabaseTransactions:
    """Tests for database transaction management."""

    def test_use_creates_session(self, mock_global_path):
        """Test that use() creates a session."""
        Database._client_lazy = None

        with patch.object(Database, "_init_client") as mock_init:
            mock_session = MagicMock()
            mock_factory = MagicMock(return_value=mock_session)
            mock_init.return_value = mock_factory

            result = Database.use(lambda session: "test_result")

            assert result == "test_result"
            mock_session.commit.assert_called_once()
            mock_session.close.assert_called_once()

    def test_use_rollback_on_error(self, mock_global_path):
        """Test that use() rolls back on error."""
        Database._client_lazy = None

        with patch.object(Database, "_init_client") as mock_init:
            mock_session = MagicMock()
            mock_factory = MagicMock(return_value=mock_session)
            mock_init.return_value = mock_factory

            with pytest.raises(ValueError):
                Database.use(lambda session: (_ for _ in ()).throw(ValueError("test error")))

            mock_session.rollback.assert_called_once()
            mock_session.close.assert_called_once()

    def test_effect_runs_after_transaction(self, mock_global_path):
        """Test that effects run after transaction completes."""
        Database._client_lazy = None
        effect_called = []

        with patch.object(Database, "_init_client") as mock_init:
            mock_session = MagicMock()
            mock_factory = MagicMock(return_value=mock_session)
            mock_init.return_value = mock_factory

            def callback(session):
                Database.effect(lambda: effect_called.append(True))
                return "result"

            result = Database.use(callback)

            assert result == "result"
            assert len(effect_called) == 1

    def test_transaction_reuses_existing_context(self, mock_global_path):
        """Test that nested transactions reuse context."""
        Database._client_lazy = None

        with patch.object(Database, "_init_client") as mock_init:
            mock_session = MagicMock()
            mock_factory = MagicMock(return_value=mock_session)
            mock_init.return_value = mock_factory

            def inner_callback(session):
                return "inner"

            def outer_callback(session):
                return Database.transaction(inner_callback)

            result = Database.use(outer_callback)

            assert result == "inner"
            # Should only commit once for outer transaction
            assert mock_session.commit.call_count == 1
