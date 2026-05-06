from app.modules.activity_logs.activity_schemas import (
    ActivityLogListResponse,
    ActivityLogRead,
)
from app.shared.dates import format_archive_date, serialize_datetime


ACTION_LABELS = {
    "game_created": "GAME CREATED",
    "game_updated": "GAME UPDATED",
    "game_deleted": "GAME DELETED",
    "rating_created": "RATING CREATED",
    "rating_updated": "RATING UPDATED",
    "rating_deleted": "RATING DELETED",
    "cover_uploaded": "COVER UPLOADED",
    "cover_updated": "COVER UPDATED",
    "archive_sync": "ARCHIVE SYNC",
}


def _get_value(source, key: str, default=None):
    if source is None:
        return default

    if isinstance(source, dict):
        return source.get(key, default)

    return getattr(source, key, default)


def get_action_label(action: str | None) -> str:
    if action is None:
        return "UNKNOWN"

    return ACTION_LABELS.get(action, action.replace("_", " ").upper())


def map_activity_log(log) -> ActivityLogRead:
    created_at = serialize_datetime(_get_value(log, "created_at"))

    return ActivityLogRead(
        id=_get_value(log, "id"),
        series_id=_get_value(log, "series_id"),
        action=_get_value(log, "action"),
        action_label=get_action_label(_get_value(log, "action")),
        message=_get_value(log, "message"),
        previous_value=_get_value(log, "previous_value"),
        new_value=_get_value(log, "new_value"),
        created_at=created_at,
        display_date=format_archive_date(created_at),
    )


def map_activity_log_list(
    logs: list,
    total: int | None = None,
    limit: int = 10,
) -> ActivityLogListResponse:
    items = [map_activity_log(log) for log in logs]

    return ActivityLogListResponse(
        items=items,
        total=len(items) if total is None else total,
        limit=limit,
    )
