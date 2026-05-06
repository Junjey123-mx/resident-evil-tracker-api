from math import ceil
from typing import Any

from app.modules.archive_entries.archive_entry_schemas import (
    ArchiveEntryDetail,
    ArchiveEntryListItem,
    ArchiveEntryListResponse,
    ArchiveEntryRead,
)
from app.shared.dates import serialize_datetime
from app.shared.file_codes import build_file_code
from app.shared.labels import (
    get_category_label,
    get_status_label,
    get_threat_level_label,
)


def _get_value(source, key: str, default=None):
    if source is None:
        return default

    if isinstance(source, dict):
        return source.get(key, default)

    return getattr(source, key, default)


def _get_engine_value(entry) -> str | None:
    engine = _get_value(entry, "engine")
    if engine is not None:
        return engine

    return _get_value(entry, "engine_name")


def _get_entry_id(entry) -> int:
    entry_id = _get_value(entry, "id", 0)

    if entry_id is None:
        return 0

    return entry_id


def _serialize_updated_at(entry):
    updated_at = serialize_datetime(_get_value(entry, "updated_at"))
    if updated_at is not None:
        return updated_at

    return serialize_datetime(_get_value(entry, "created_at"))


def _serialize_estimated_duration(entry) -> int | None:
    value = _get_value(entry, "estimated_duration")

    if value is None:
        return None

    if isinstance(value, int):
        return value

    if isinstance(value, str) and value.isdigit():
        return int(value)

    return None


def format_display_score(score: float | None) -> str:
    if score is None:
        return "N/A"

    return f"{score:.1f}/10"


def _format_survival_index(survival_index: int | None) -> str:
    if survival_index is None:
        return "N/A"

    return f"{survival_index}/100"


def _base_archive_entry_payload(entry) -> dict[str, Any]:
    return {
        "id": _get_entry_id(entry),
        "title": _get_value(entry, "title"),
        "release_year": _get_value(entry, "release_year"),
        "main_protagonist": _get_value(entry, "main_protagonist"),
        "original_platform": _get_value(entry, "original_platform"),
        "chronology_order": _get_value(entry, "chronology_order"),
        "description": _get_value(entry, "description"),
        "cover_image_url": _get_value(entry, "cover_image_url"),
        "cover_image_public_id": _get_value(entry, "cover_image_public_id"),
        "category": _get_value(entry, "category"),
        "status": _get_value(entry, "status"),
        "threat_level": _get_value(entry, "threat_level"),
        "director": _get_value(entry, "director"),
        "developer": _get_value(entry, "developer"),
        "genre": _get_value(entry, "genre"),
        "engine": _get_engine_value(entry),
        "umbrella_classification": _get_value(entry, "umbrella_classification"),
        "survival_index": _get_value(entry, "survival_index"),
        "players": _get_value(entry, "players"),
        "estimated_duration": _serialize_estimated_duration(entry),
        "chronology_era": _get_value(entry, "chronology_era"),
        "alias_title": _get_value(entry, "alias_title"),
        "main_locations": _get_value(entry, "main_locations"),
        "threat_type": _get_value(entry, "threat_type"),
        "registered_platforms": _get_value(entry, "registered_platforms"),
        "created_at": serialize_datetime(_get_value(entry, "created_at")),
        "updated_at": _serialize_updated_at(entry),
    }


def map_archive_entry_read(entry) -> ArchiveEntryRead:
    return ArchiveEntryRead(**_base_archive_entry_payload(entry))


def map_archive_entry_list_item(
    entry,
    rating_score: float | None = None,
) -> ArchiveEntryListItem:
    category = _get_value(entry, "category")
    status = _get_value(entry, "status")
    threat_level = _get_value(entry, "threat_level")

    return ArchiveEntryListItem(
        id=_get_entry_id(entry),
        file_code=build_file_code(_get_entry_id(entry)),
        title=_get_value(entry, "title"),
        release_year=_get_value(entry, "release_year"),
        main_protagonist=_get_value(entry, "main_protagonist"),
        original_platform=_get_value(entry, "original_platform"),
        chronology_order=_get_value(entry, "chronology_order"),
        cover_image_url=_get_value(entry, "cover_image_url"),
        category=category,
        category_label=get_category_label(category),
        status=status,
        status_label=get_status_label(status),
        threat_level=threat_level,
        threat_level_label=get_threat_level_label(threat_level),
        rating_score=rating_score,
        display_score=format_display_score(rating_score),
        created_at=serialize_datetime(_get_value(entry, "created_at")),
    )


def map_archive_entry_detail(
    entry,
    rating_score: float | None = None,
    personal_review: str | None = None,
    related_entries: list | None = None,
    activity_summary: list | None = None,
) -> ArchiveEntryDetail:
    category = _get_value(entry, "category")
    status = _get_value(entry, "status")
    threat_level = _get_value(entry, "threat_level")
    survival_index = _get_value(entry, "survival_index")

    return ArchiveEntryDetail(
        **_base_archive_entry_payload(entry),
        file_code=build_file_code(_get_entry_id(entry)),
        category_label=get_category_label(category),
        status_label=get_status_label(status),
        threat_level_label=get_threat_level_label(threat_level),
        display_survival_index=_format_survival_index(survival_index),
        rating_score=rating_score,
        display_score=format_display_score(rating_score),
        personal_review=personal_review,
        related_entries=related_entries,
        activity_summary=activity_summary,
    )


def map_archive_entry_list_response(
    entries: list,
    total: int,
    page: int,
    limit: int,
    rating_scores: dict[int, float] | None = None,
) -> ArchiveEntryListResponse:
    safe_limit = limit if limit > 0 else 1
    pages = ceil(total / safe_limit) if total > 0 else 0
    scores = rating_scores or {}

    items = [
        map_archive_entry_list_item(
            entry,
            rating_score=scores.get(_get_entry_id(entry)),
        )
        for entry in entries
    ]

    return ArchiveEntryListResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=pages,
        has_next=page < pages,
        has_previous=page > 1 and pages > 0,
    )
