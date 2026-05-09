from app.modules.activity_logs.activity_mapper import get_action_label
from app.modules.dashboard.dashboard_schemas import (
    DashboardActivityItem,
    DashboardFeaturedEntry,
    DashboardRecentEntry,
    DashboardStatsResponse,
    DashboardTimelineItem,
    DashboardTopRatedItem,
)
from app.modules.personal_ratings.rating_mapper import format_rating_score
from app.shared.dates import format_archive_date, serialize_datetime
from app.shared.file_codes import build_file_code
from app.shared.labels import get_category_label, get_status_label


def _get_value(source, key: str, default=None):
    if source is None:
        return default

    if isinstance(source, dict):
        return source.get(key, default)

    return getattr(source, key, default)


def map_featured_entry(entry, rating_score: float | None = None) -> DashboardFeaturedEntry | None:
    if entry is None:
        return None

    entry_id = _get_value(entry, "id")
    return DashboardFeaturedEntry(
        id=entry_id,
        file_code=build_file_code(entry_id),
        title=_get_value(entry, "title"),
        release_year=_get_value(entry, "release_year"),
        cover_image_url=_get_value(entry, "cover_image_url"),
        rating_score=rating_score,
        display_score=format_rating_score(rating_score),
    )


def map_recent_entry(entry) -> DashboardRecentEntry:
    category = _get_value(entry, "category")
    status = _get_value(entry, "status")
    entry_id = _get_value(entry, "id")

    return DashboardRecentEntry(
        id=entry_id,
        file_code=build_file_code(entry_id),
        title=_get_value(entry, "title"),
        release_year=_get_value(entry, "release_year"),
        category=category,
        category_label=get_category_label(category),
        status=status,
        status_label=get_status_label(status),
        cover_image_url=_get_value(entry, "cover_image_url"),
        created_at=serialize_datetime(_get_value(entry, "created_at")),
    )


def map_timeline_item(release_year: int, total: int) -> DashboardTimelineItem:
    return DashboardTimelineItem(release_year=release_year, total=total)


def map_top_rated_entry(entry, rating_score: float) -> DashboardTopRatedItem:
    entry_id = _get_value(entry, "id")
    return DashboardTopRatedItem(
        id=entry_id,
        file_code=build_file_code(entry_id),
        title=_get_value(entry, "title"),
        release_year=_get_value(entry, "release_year"),
        rating_score=rating_score,
        display_score=format_rating_score(rating_score),
    )


def map_dashboard_activity(log) -> DashboardActivityItem:
    created_at = serialize_datetime(_get_value(log, "created_at"))
    action = _get_value(log, "action")

    return DashboardActivityItem(
        id=_get_value(log, "id"),
        series_id=_get_value(log, "series_id"),
        action=action,
        action_label=get_action_label(action),
        message=_get_value(log, "message"),
        display_date=format_archive_date(created_at),
        created_at=created_at,
    )


def build_dashboard_stats_response(
    total_entries: int,
    average_rating: float | None,
    best_rated_entry: DashboardFeaturedEntry | None,
    latest_entry: DashboardFeaturedEntry | None,
    recent_entries: list[DashboardRecentEntry],
    release_timeline: list[DashboardTimelineItem],
    top_rated_entries: list[DashboardTopRatedItem],
    recent_activity: list[DashboardActivityItem],
) -> DashboardStatsResponse:
    return DashboardStatsResponse(
        total_entries=total_entries,
        average_rating=average_rating,
        display_average_rating=format_rating_score(average_rating),
        best_rated_entry=best_rated_entry,
        latest_entry=latest_entry,
        recent_entries=recent_entries,
        release_timeline=release_timeline,
        top_rated_entries=top_rated_entries,
        recent_activity=recent_activity,
    )
