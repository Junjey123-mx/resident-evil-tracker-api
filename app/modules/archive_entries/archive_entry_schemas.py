from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


ArchiveEntryCategory = Literal[
    "main_series",
    "remake",
    "prequel",
    "spin_off",
    "expansion",
]
ArchiveEntryStatus = Literal["registered", "pending", "archived"]
ArchiveEntryThreatLevel = Literal["low", "medium", "high", "critical"]
ArchiveEntrySortField = Literal[
    "title",
    "release_year",
    "chronology_order",
    "rating",
    "created_at",
]
SortOrder = Literal["asc", "desc"]


class ArchiveEntryBase(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    release_year: int = Field(ge=1996, le=2026)
    main_protagonist: str = Field(min_length=1, max_length=120)
    original_platform: str = Field(min_length=1, max_length=120)
    chronology_order: int = Field(gt=0)
    description: str = Field(min_length=10, max_length=1000)
    cover_image_url: Optional[str] = None
    cover_image_public_id: Optional[str] = None
    category: Optional[ArchiveEntryCategory] = None
    status: Optional[ArchiveEntryStatus] = None
    threat_level: Optional[ArchiveEntryThreatLevel] = None
    director: Optional[str] = Field(default=None, max_length=120)
    developer: Optional[str] = Field(default=None, max_length=120)
    genre: Optional[str] = Field(default=None, max_length=120)
    engine: Optional[str] = Field(default=None, max_length=120)
    umbrella_classification: Optional[str] = Field(default=None, max_length=120)
    survival_index: Optional[int] = Field(default=None, ge=0, le=100)
    players: Optional[int] = Field(default=None, ge=1)
    estimated_duration: Optional[int] = Field(default=None, ge=0)
    chronology_era: Optional[str] = Field(default=None, max_length=120)
    alias_title: Optional[str] = Field(default=None, max_length=150)
    main_locations: Optional[str] = None
    threat_type: Optional[str] = Field(default=None, max_length=120)
    registered_platforms: Optional[str] = None


class ArchiveEntryCreate(ArchiveEntryBase):
    """Payload for creating a franchise archive entry."""


class ArchiveEntryUpdate(BaseModel):
    """Payload for partially updating a franchise archive entry."""

    title: Optional[str] = Field(default=None, min_length=2, max_length=150)
    release_year: Optional[int] = Field(default=None, ge=1996, le=2026)
    main_protagonist: Optional[str] = Field(default=None, min_length=1, max_length=120)
    original_platform: Optional[str] = Field(default=None, min_length=1, max_length=120)
    chronology_order: Optional[int] = Field(default=None, gt=0)
    description: Optional[str] = Field(default=None, min_length=10, max_length=1000)
    cover_image_url: Optional[str] = None
    cover_image_public_id: Optional[str] = None
    category: Optional[ArchiveEntryCategory] = None
    status: Optional[ArchiveEntryStatus] = None
    threat_level: Optional[ArchiveEntryThreatLevel] = None
    director: Optional[str] = Field(default=None, max_length=120)
    developer: Optional[str] = Field(default=None, max_length=120)
    genre: Optional[str] = Field(default=None, max_length=120)
    engine: Optional[str] = Field(default=None, max_length=120)
    umbrella_classification: Optional[str] = Field(default=None, max_length=120)
    survival_index: Optional[int] = Field(default=None, ge=0, le=100)
    players: Optional[int] = Field(default=None, ge=1)
    estimated_duration: Optional[int] = Field(default=None, ge=0)
    chronology_era: Optional[str] = Field(default=None, max_length=120)
    alias_title: Optional[str] = Field(default=None, max_length=150)
    main_locations: Optional[str] = None
    threat_type: Optional[str] = Field(default=None, max_length=120)
    registered_platforms: Optional[str] = None


class ArchiveEntryRead(ArchiveEntryBase):
    """Base response contract for a franchise archive entry."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class ArchiveEntryListItem(BaseModel):
    """Compact response contract for archive cards and listings."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    file_code: str
    title: str
    release_year: int
    main_protagonist: str
    original_platform: str
    chronology_order: int
    cover_image_url: Optional[str] = None
    category: Optional[ArchiveEntryCategory] = None
    category_label: str
    status: Optional[ArchiveEntryStatus] = None
    status_label: str
    threat_level: Optional[ArchiveEntryThreatLevel] = None
    threat_level_label: str
    rating_score: Optional[float] = None
    display_score: Optional[str] = None
    created_at: datetime


class ArchiveEntryDetail(ArchiveEntryRead):
    """Detailed response contract for a single archive entry."""

    file_code: str
    category_label: str
    status_label: str
    threat_level_label: str
    display_survival_index: Optional[str] = None
    rating_score: Optional[float] = None
    display_score: Optional[str] = None
    personal_review: Optional[str] = None
    related_entries: Optional[list[dict[str, Any]]] = None
    activity_summary: Optional[list[dict[str, Any]]] = None


class ArchiveEntryListResponse(BaseModel):
    """Paginated response contract for archive listings."""

    items: list[ArchiveEntryListItem]
    total: int
    page: int
    limit: int
    pages: int
    has_next: bool
    has_previous: bool


class ArchiveEntryQueryParams(BaseModel):
    """Validated query parameters for archive listings."""

    q: Optional[str] = None
    sort: ArchiveEntrySortField = "title"
    order: SortOrder = "asc"
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=8, ge=1, le=50)
