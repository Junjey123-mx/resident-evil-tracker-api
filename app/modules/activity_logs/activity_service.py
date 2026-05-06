from fastapi import HTTPException
from sqlmodel import Session

from app.modules.activity_logs.activity_mapper import map_activity_log_list
from app.modules.activity_logs.activity_repository import ActivityLogRepository
from app.modules.activity_logs.activity_schemas import ActivityLogListResponse
from app.modules.archive_entries.archive_entry_repository import ArchiveEntryRepository


ENTRY_NOT_FOUND_MESSAGE = "No se encontró el registro solicitado."


class ActivityLogService:
    def __init__(self, session: Session):
        self.session = session
        self.activity_repository = ActivityLogRepository(session)
        self.archive_repository = ArchiveEntryRepository(session)

    def list_recent_activity(self, limit: int = 10) -> ActivityLogListResponse:
        logs = self.activity_repository.list_recent(n=limit)
        total = self.activity_repository.count()
        return map_activity_log_list(logs, total=total, limit=limit)

    def list_activity_by_series_id(
        self,
        series_id: int,
        limit: int = 10,
    ) -> ActivityLogListResponse:
        if not self.archive_repository.exists(series_id):
            raise HTTPException(status_code=404, detail=ENTRY_NOT_FOUND_MESSAGE)

        logs = self.activity_repository.list_by_series_id(series_id, limit=limit)
        total = self.activity_repository.count_by_series_id(series_id)
        return map_activity_log_list(logs, total=total, limit=limit)
