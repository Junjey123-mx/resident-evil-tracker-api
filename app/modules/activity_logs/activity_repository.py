from typing import Optional

from sqlalchemy import func
from sqlmodel import Session, select

from app.modules.activity_logs.activity_model import ActivityLog


class ActivityLogRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, id: int) -> Optional[ActivityLog]:
        return self.session.get(ActivityLog, id)

    def list_by_series(self, series_id: int) -> list[ActivityLog]:
        stmt = (
            select(ActivityLog)
            .where(ActivityLog.series_id == series_id)
            .order_by(ActivityLog.created_at.desc())
        )
        return list(self.session.exec(stmt).all())

    def list_by_series_id(self, series_id: int, limit: int = 20) -> list[ActivityLog]:
        stmt = (
            select(ActivityLog)
            .where(ActivityLog.series_id == series_id)
            .order_by(ActivityLog.created_at.desc())
            .limit(limit)
        )
        return list(self.session.exec(stmt).all())

    def list_recent(self, n: int = 10) -> list[ActivityLog]:
        stmt = select(ActivityLog).order_by(ActivityLog.created_at.desc()).limit(n)
        return list(self.session.exec(stmt).all())

    def count(self) -> int:
        result = self.session.exec(select(func.count()).select_from(ActivityLog))
        return result.one()

    def count_by_series_id(self, series_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(ActivityLog)
            .where(ActivityLog.series_id == series_id)
        )
        result = self.session.exec(stmt)
        return result.one()

    def count_by_action(self) -> dict[str, int]:
        stmt = select(ActivityLog.action, func.count()).group_by(ActivityLog.action)
        rows = self.session.exec(stmt).all()
        return {action: total for action, total in rows}

    def create(self, data: dict) -> ActivityLog:
        log = ActivityLog(**data)
        self.session.add(log)
        self.session.flush()
        self.session.refresh(log)
        return log

    def exists_for_series_action(self, series_id: Optional[int], action: str) -> bool:
        if series_id is None:
            stmt = select(ActivityLog.id).where(
                ActivityLog.series_id.is_(None),  # type: ignore[union-attr]
                ActivityLog.action == action,
            )
        else:
            stmt = select(ActivityLog.id).where(
                ActivityLog.series_id == series_id,
                ActivityLog.action == action,
            )
        return self.session.exec(stmt).first() is not None
