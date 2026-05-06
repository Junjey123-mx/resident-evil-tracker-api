from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func, or_
from sqlmodel import Session, select

from app.modules.archive_entries.archive_entry_model import ArchiveEntry
from app.modules.personal_ratings.rating_model import Rating
from app.shared.pagination import calculate_offset
from app.shared.sorting import is_desc_order

_SORT_COLUMN_MAP: dict[str, str] = {
    "title": "title",
    "release_year": "release_year",
    "chronology_order": "chronology_order",
    "created_at": "created_at",
    "updated_at": "updated_at",
}

# Fields that arrive from the API under a different key than the ORM attribute.
_KEY_REMAP = {"engine": "engine_name"}


class ArchiveEntryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, id: int) -> Optional[ArchiveEntry]:
        return self.session.get(ArchiveEntry, id)

    def get_by_title(self, title: str) -> Optional[ArchiveEntry]:
        stmt = select(ArchiveEntry).where(ArchiveEntry.title == title)
        return self.session.exec(stmt).first()

    def get_all(self) -> list[ArchiveEntry]:
        return list(self.session.exec(select(ArchiveEntry)).all())

    def list_all(self) -> list[ArchiveEntry]:
        return self.get_all()

    def list_paginated(
        self,
        offset: int = 0,
        limit: int = 20,
        sort_by: str = "chronology_order",
        sort_order: str = "asc",
        q: str | None = None,
        sort: str | None = None,
        order: str | None = None,
        page: int | None = None,
    ) -> list[ArchiveEntry]:
        effective_sort = sort or sort_by
        effective_order = order or sort_order
        effective_offset = calculate_offset(page, limit) if page is not None else offset

        stmt = self._base_list_statement(q)

        if effective_sort == "rating":
            stmt = stmt.outerjoin(Rating, Rating.series_id == ArchiveEntry.id)
            rating_order = Rating.score.desc() if is_desc_order(effective_order) else Rating.score.asc()
            stmt = stmt.order_by(rating_order.nulls_last(), ArchiveEntry.title.asc())
        else:
            col_name = _SORT_COLUMN_MAP.get(effective_sort, "chronology_order")
            col = getattr(ArchiveEntry, col_name)
            order_expr = col.desc() if is_desc_order(effective_order) else col.asc()
            stmt = stmt.order_by(order_expr, ArchiveEntry.id.asc())

        stmt = stmt.offset(effective_offset).limit(limit)
        return list(self.session.exec(stmt).all())

    def get_recent(self, n: int = 5) -> list[ArchiveEntry]:
        stmt = select(ArchiveEntry).order_by(ArchiveEntry.created_at.desc()).limit(n)
        return list(self.session.exec(stmt).all())

    def count_by_release_year(self) -> list[tuple[int, int]]:
        stmt = (
            select(ArchiveEntry.release_year, func.count())
            .group_by(ArchiveEntry.release_year)
            .order_by(ArchiveEntry.release_year.asc())
        )
        rows = self.session.exec(stmt).all()
        return [(release_year, total) for release_year, total in rows]

    def count(self) -> int:
        result = self.session.exec(select(func.count()).select_from(ArchiveEntry))
        return result.one()

    def count_filtered(self, q: str | None = None) -> int:
        stmt = select(func.count()).select_from(ArchiveEntry)
        search_filter = self._build_search_filter(q)
        if search_filter is not None:
            stmt = stmt.where(search_filter)
        result = self.session.exec(stmt)
        return result.one()

    def exists(self, id: int) -> bool:
        stmt = select(ArchiveEntry.id).where(ArchiveEntry.id == id)
        return self.session.exec(stmt).first() is not None

    def create(self, data: dict) -> ArchiveEntry:
        remapped = {_KEY_REMAP.get(k, k): v for k, v in data.items()}
        entry = ArchiveEntry(**remapped)
        self.session.add(entry)
        self.session.flush()
        self.session.refresh(entry)
        return entry

    def update(self, id: int, data: dict) -> Optional[ArchiveEntry]:
        entry = self.session.get(ArchiveEntry, id)
        if entry is None:
            return None
        remapped = {_KEY_REMAP.get(k, k): v for k, v in data.items()}
        for attr, value in remapped.items():
            setattr(entry, attr, value)
        entry.updated_at = datetime.now(timezone.utc)
        self.session.add(entry)
        self.session.flush()
        self.session.refresh(entry)
        return entry

    def delete(self, id: int) -> bool:
        entry = self.session.get(ArchiveEntry, id)
        if entry is None:
            return False
        self.session.delete(entry)
        self.session.flush()
        return True

    def _base_list_statement(self, q: str | None = None):
        stmt = select(ArchiveEntry)
        search_filter = self._build_search_filter(q)
        if search_filter is not None:
            stmt = stmt.where(search_filter)
        return stmt

    def _build_search_filter(self, q: str | None = None):
        if q is None or not q.strip():
            return None

        pattern = f"%{q.strip()}%"
        return or_(
            ArchiveEntry.title.ilike(pattern),
            ArchiveEntry.main_protagonist.ilike(pattern),
            ArchiveEntry.original_platform.ilike(pattern),
            ArchiveEntry.description.ilike(pattern),
            ArchiveEntry.category.ilike(pattern),
            ArchiveEntry.status.ilike(pattern),
            ArchiveEntry.threat_level.ilike(pattern),
        )
