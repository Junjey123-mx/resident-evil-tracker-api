from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DashboardFeaturedEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    file_code: Optional[str] = None
    title: Optional[str] = None
    release_year: Optional[int] = None
    cover_image_url: Optional[str] = None
    rating_score: Optional[float] = None
    display_score: Optional[str] = None


class DashboardRecentEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_code: str
    title: str
    release_year: int
    category: Optional[str] = None
    category_label: str
    status: Optional[str] = None
    status_label: str
    cover_image_url: Optional[str] = None
    created_at: datetime


class DashboardTimelineItem(BaseModel):
    release_year: int
    total: int


class DashboardTopRatedItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_code: str
    title: str
    release_year: int
    rating_score: float
    display_score: str


class DashboardActivityItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    series_id: Optional[int] = None
    action: str
    action_label: str
    message: str
    display_date: Optional[str] = None
    created_at: datetime


class DashboardStatsResponse(BaseModel):
    total_entries: int
    average_rating: Optional[float] = None
    display_average_rating: str
    best_rated_entry: Optional[DashboardFeaturedEntry] = None
    latest_entry: Optional[DashboardFeaturedEntry] = None
    recent_entries: list[DashboardRecentEntry]
    release_timeline: list[DashboardTimelineItem]
    top_rated_entries: list[DashboardTopRatedItem]
    recent_activity: list[DashboardActivityItem]
