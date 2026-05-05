from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import CheckConstraint, Column, DateTime, Index, String, Text
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.activity_logs.activity_model import ActivityLog
    from app.modules.personal_ratings.rating_model import Rating


class ArchiveEntry(SQLModel, table=True):
    """ORM model for the 'series' table — central franchise archive entry."""

    __tablename__ = "series"

    __table_args__ = (
        # --- Column-level constraints mirroring schema.sql CHECK expressions ---
        CheckConstraint(
            "release_year BETWEEN 1996 AND 2026",
            name="ck_series_release_year",
        ),
        CheckConstraint(
            "chronology_order > 0",
            name="ck_series_chronology_order",
        ),
        CheckConstraint(
            "category IN ('main_series','remake','prequel','spin_off','expansion')",
            name="ck_series_category",
        ),
        CheckConstraint(
            "status IN ('registered','pending','archived')",
            name="ck_series_status",
        ),
        CheckConstraint(
            "threat_level IN ('low','medium','high','critical')",
            name="ck_series_threat_level",
        ),
        CheckConstraint(
            "survival_index BETWEEN 0 AND 100",
            name="ck_series_survival_index",
        ),
        CheckConstraint(
            "players >= 1",
            name="ck_series_players",
        ),
        # --- Indexes mirroring schema.sql ---
        Index("idx_series_title", "title"),
        Index("idx_series_release_year", "release_year"),
        Index("idx_series_chronology_order", "chronology_order"),
        Index("idx_series_category", "category"),
        Index("idx_series_status", "status"),
        Index("idx_series_threat_level", "threat_level"),
        Index("idx_series_created_at", "created_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    # --- Core identity ---
    title: str = Field(max_length=255)
    alias_title: Optional[str] = Field(default=None, max_length=255)
    release_year: int = Field()
    main_protagonist: str = Field(max_length=100)
    original_platform: str = Field(max_length=100)
    registered_platforms: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
    )
    chronology_order: int = Field()
    chronology_era: Optional[str] = Field(default=None, max_length=100)

    # --- Narrative & editorial ---
    description: str = Field(sa_column=Column(Text, nullable=False))
    category: str = Field(max_length=20)
    status: str = Field(max_length=20)
    threat_level: str = Field(max_length=10)
    umbrella_classification: Optional[str] = Field(default=None, max_length=100)
    threat_type: Optional[str] = Field(default=None, max_length=100)
    main_locations: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
    )

    # --- Production metadata ---
    director: Optional[str] = Field(default=None, max_length=100)
    developer: Optional[str] = Field(default=None, max_length=100)
    genre: Optional[str] = Field(default=None, max_length=100)

    # SQL column is named "engine"; engine_name avoids collision with SQLAlchemy's Engine class.
    engine_name: Optional[str] = Field(
        default=None,
        sa_column=Column("engine", String(100), nullable=True),
    )

    # --- Gameplay ---
    players: Optional[int] = Field(default=None)
    estimated_duration: Optional[int] = Field(default=None)  # stored in minutes
    survival_index: Optional[int] = Field(default=None)

    # --- Cover image (managed via Cloudinary) ---
    cover_image_url: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
    )
    cover_image_public_id: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
    )

    # --- Timestamps — TIMESTAMPTZ in PostgreSQL ---
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    # --- Relationships ---
    # back_populates must match the attribute name on the other model
    rating: Optional["Rating"] = Relationship(back_populates="series")
    activity_logs: List["ActivityLog"] = Relationship(back_populates="series")
