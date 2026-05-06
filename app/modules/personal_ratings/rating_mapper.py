from app.modules.personal_ratings.rating_schemas import RatingRead
from app.shared.dates import serialize_datetime


def _get_value(source, key: str, default=None):
    if source is None:
        return default

    if isinstance(source, dict):
        return source.get(key, default)

    return getattr(source, key, default)


def format_rating_score(score: float | None) -> str:
    if score is None:
        return "N/A"

    return f"{score:.1f}/10"


def map_rating_read(rating) -> RatingRead:
    score = _get_value(rating, "score")
    created_at = serialize_datetime(_get_value(rating, "created_at"))
    updated_at = serialize_datetime(_get_value(rating, "updated_at")) or created_at

    return RatingRead(
        id=_get_value(rating, "id"),
        series_id=_get_value(rating, "series_id"),
        score=float(score),
        display_score=format_rating_score(float(score)),
        review=_get_value(rating, "review"),
        created_at=created_at,
        updated_at=updated_at,
    )
