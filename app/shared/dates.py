from datetime import date, datetime


def serialize_datetime(value) -> datetime | None:
    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())

    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None

    return None


def format_archive_date(value) -> str | None:
    serialized = serialize_datetime(value)

    if serialized is None:
        return value if isinstance(value, str) and value else None

    return serialized.date().isoformat()
