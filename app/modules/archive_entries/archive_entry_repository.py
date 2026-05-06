from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func
from sqlmodel import Session, select

from app.modules.archive_entries.archive_entry_model import ArchiveEntry

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
    ) -> list[ArchiveEntry]:
        col_name = _SORT_COLUMN_MAP.get(sort_by, "chronology_order")
        col = getattr(ArchiveEntry, col_name)
        order_expr = col.desc() if sort_order.lower() == "desc" else col.asc()
        stmt = select(ArchiveEntry).order_by(order_expr).offset(offset).limit(limit)
        return list(self.session.exec(stmt).all())

    def get_recent(self, n: int = 5) -> list[ArchiveEntry]:
        stmt = select(ArchiveEntry).order_by(ArchiveEntry.created_at.desc()).limit(n)
        return list(self.session.exec(stmt).all())

    def count(self) -> int:
        result = self.session.exec(select(func.count()).select_from(ArchiveEntry))
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
