"""Database connection and transaction management."""

import os
import re
from collections.abc import Callable
from contextvars import ContextVar
from datetime import datetime
from pathlib import Path
from typing import Any, TypeVar

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from langcode.util.lazy import Lazy
from langcode.util.log import Log

T = TypeVar("T")

log = Log.create(service="db")


class NotFoundError(Exception):
    """Resource not found in database."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class Database:
    """Database connection and transaction management."""

    Path: str = ""
    _engine: Any = None
    _session_factory: Any = None
    _ctx: ContextVar[dict[str, Any] | None] = ContextVar("database", default=None)
    _client_lazy: Any = None

    @classmethod
    def _get_db_path(cls) -> str:
        """Get database path based on channel and flags."""
        from langcode.flag.flag import Flag
        from langcode.global_config import Global
        from langcode.installation import Installation

        channel = Installation.CHANNEL
        data_dir = Global.Path.data

        if channel in ["latest", "beta"] or Flag.OPENCODE_DISABLE_CHANNEL_DB:
            return os.path.join(data_dir, "opencode.db")

        # Sanitize channel name for filename
        safe_channel = "".join(c if c.isalnum() or c in "._-" else "-" for c in channel)
        return os.path.join(data_dir, f"opencode-{safe_channel}.db")

    @classmethod
    def _init_client(cls) -> sessionmaker:
        """Initialize database client with migrations."""
        cls.Path = cls._get_db_path()
        log.info("opening database", path=cls.Path)

        # Ensure directory exists
        Path(cls.Path).parent.mkdir(parents=True, exist_ok=True)

        # Create engine with SQLite optimizations
        cls._engine = create_engine(
            f"sqlite:///{cls.Path}",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        # Set SQLite pragmas
        @event.listens_for(cls._engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA journal_mode = WAL")
            cursor.execute("PRAGMA synchronous = NORMAL")
            cursor.execute("PRAGMA busy_timeout = 5000")
            cursor.execute("PRAGMA cache_size = -64000")
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute("PRAGMA wal_checkpoint(PASSIVE)")
            cursor.close()

        # Apply migrations
        cls._apply_migrations()

        cls._session_factory = sessionmaker(bind=cls._engine)
        return cls._session_factory

    @classmethod
    def _apply_migrations(cls):
        """Apply database migrations."""
        from langcode.flag.flag import Flag

        migration_dir = Path(__file__).parent.parent.parent.parent / "migration"

        if not migration_dir.exists():
            log.info("no migrations directory found")
            return

        # Get all migration directories sorted by timestamp
        migrations = []
        for entry in sorted(migration_dir.iterdir()):
            if not entry.is_dir():
                continue
            migration_file = entry / "migration.sql"
            if not migration_file.exists():
                continue

            # Parse timestamp from directory name (format: YYYYMMDDHHMMSS_name)
            name = entry.name
            timestamp = cls._parse_migration_timestamp(name)

            migrations.append({"sql": migration_file.read_text(), "timestamp": timestamp, "name": name})

        if migrations:
            log.info("applying migrations", count=len(migrations))

            if Flag.OPENCODE_SKIP_MIGRATIONS:
                for migration in migrations:
                    migration["sql"] = "SELECT 1;"

            # Apply migrations
            with cls._engine.begin() as conn:
                for migration in migrations:
                    try:
                        conn.execute(migration["sql"])
                    except Exception as e:
                        log.error(
                            "migration failed",
                            name=migration["name"],
                            error=str(e),
                        )
                        raise

    @classmethod
    def _parse_migration_timestamp(cls, name: str) -> int:
        """Parse timestamp from migration directory name."""

        match = re.match(r"^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})", name)
        if not match:
            return 0

        dt = datetime(
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
            int(match.group(4)),
            int(match.group(5)),
            int(match.group(6)),
        )
        return int(dt.timestamp() * 1000)

    @classmethod
    def client(cls) -> sessionmaker:
        """Get or create database client."""
        if cls._client_lazy is None:
            cls._client_lazy = Lazy(lambda: cls._init_client())
        return cls._client_lazy()

    @classmethod
    def close(cls):
        """Close database connection."""
        if cls._engine:
            cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None
            if cls._client_lazy:
                cls._client_lazy.reset()
                cls._client_lazy = None

    @classmethod
    def use(cls, callback: Callable[[Session], T]) -> T:
        """Execute callback with database session."""
        ctx_data = cls._ctx.get()

        if ctx_data is not None:
            # Already in a context, reuse session
            return callback(ctx_data["session"])

        # Create new session and context
        session_factory = cls.client()
        session = session_factory()
        effects: list[Callable[[], Any]] = []

        try:
            ctx_data = {"session": session, "effects": effects}
            token = cls._ctx.set(ctx_data)
            try:
                result = callback(session)
                session.commit()
                return result
            finally:
                cls._ctx.reset(token)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            # Run effects after session is closed
            for effect in effects:
                effect()

    @classmethod
    def effect(cls, fn: Callable[[], Any]):
        """Register effect to run after transaction completes."""
        ctx_data = cls._ctx.get()
        if ctx_data is not None:
            ctx_data["effects"].append(fn)
        else:
            # No active context, run immediately
            fn()

    @classmethod
    def transaction(cls, callback: Callable[[Session], T]) -> T:
        """Execute callback in a transaction."""
        ctx_data = cls._ctx.get()

        if ctx_data is not None:
            # Already in a transaction, reuse it
            return callback(ctx_data["session"])

        # Create new transaction
        session_factory = cls.client()
        session = session_factory()
        effects: list[Callable[[], Any]] = []

        try:
            ctx_data = {"session": session, "effects": effects}
            token = cls._ctx.set(ctx_data)
            try:
                result = callback(session)
                session.commit()
                return result
            finally:
                cls._ctx.reset(token)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            # Run effects after transaction completes
            for effect in effects:
                effect()
