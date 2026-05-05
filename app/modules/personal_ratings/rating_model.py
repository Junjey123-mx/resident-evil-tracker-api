from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Index, Integer, Numeric
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.archive_entries.archive_entry_model import ArchiveEntry


class Rating(SQLModel, table=True):
    """ORM model for the 'ratings' table — one personal score per archive entry."""

    __tablename__ = "ratings"

    __table_args__ = (
        CheckConstraint(
            "score BETWEEN 1 AND 10",
            name="ck_ratings_score",
        ),
        Index("idx_ratings_series_id", "series_id"),
        Index("idx_ratings_score", "score"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    # FK to series(id) with UNIQUE (one rating per game) and CASCADE on delete.
    # ON DELETE CASCADE is expressed via sa_column because SQLModel's Field
    # foreign_key param does not expose ondelete semantics.
    series_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("series.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        )
    )

    # NUMERIC(3,1) in DB; stored as float at the Python/Pydantic layer.
    # Precision is enforced by the CHECK constraint above.
    score: float = Field(sa_column=Column(Numeric(3, 1), nullable=False))

    review: Optional[str] = Field(default=None, max_length=500)

    # --- Timestamps — TIMESTAMPTZ in PostgreSQL ---
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    # --- Relationship ---
    series: Optional["ArchiveEntry"] = Relationship(back_populates="rating")
