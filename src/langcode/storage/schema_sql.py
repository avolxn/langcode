"""SQLAlchemy schema helpers."""

from datetime import UTC, datetime

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


def get_current_timestamp() -> int:
    """Get current timestamp in milliseconds."""
    return int(datetime.now(UTC).timestamp() * 1000)


class Timestamps:
    """Mixin for timestamp columns."""

    time_created: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=get_current_timestamp,
    )
    time_updated: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=get_current_timestamp,
        onupdate=get_current_timestamp,
    )
