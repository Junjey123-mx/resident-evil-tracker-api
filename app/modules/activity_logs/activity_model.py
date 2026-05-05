from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Index, Integer, Text
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.archive_entries.archive_entry_model import ArchiveEntry


class ActivityLog(SQLModel, table=True):
    """ORM model for 'activity_logs' — append-only audit trail of all user actions."""

    __tablename__ = "activity_logs"

    __table_args__ = (
        CheckConstraint(
            "action IN ("
            "'game_created','game_updated','game_deleted',"
            "'rating_created','rating_updated','rating_deleted',"
            "'cover_uploaded','cover_updated','archive_sync'"
            ")",
            name="ck_activity_logs_action",
        ),
        Index("idx_activity_logs_series_id", "series_id"),
        Index("idx_activity_logs_action", "action"),
        Index("idx_activity_logs_created_at", "created_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    # Nullable FK to series(id) with SET NULL on delete.
    # Log entries are preserved even when the referenced series is deleted.
    # ON DELETE SET NULL expressed via sa_column because SQLModel's Field
    # foreign_key param does not expose ondelete semantics.
    series_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            Integer,
            ForeignKey("series.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    action: str = Field(max_length=30)
    message: str = Field(sa_column=Column(Text, nullable=False))
    previous_value: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
    )
    new_value: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
    )

    # --- Timestamp — TIMESTAMPTZ in PostgreSQL (no updated_at; log is append-only) ---
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    # --- Relationship ---
    series: Optional["ArchiveEntry"] = Relationship(back_populates="activity_logs")
