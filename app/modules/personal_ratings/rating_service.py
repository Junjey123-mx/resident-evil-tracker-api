from datetime import datetime, timezone

from fastapi import HTTPException
from sqlmodel import Session

# Registers ArchiveEntry relationship targets for standalone service/database usage.
from app.modules.activity_logs.activity_model import ActivityLog
from app.modules.activity_logs.activity_service import ActivityLogService
from app.modules.archive_entries.archive_entry_repository import ArchiveEntryRepository
from app.modules.personal_ratings.rating_mapper import format_rating_score, map_rating_read
from app.modules.personal_ratings.rating_repository import RatingRepository
from app.modules.personal_ratings.rating_schemas import (
    RatingCreate,
    RatingRead,
    RatingUpdate,
)


ENTRY_NOT_FOUND_MESSAGE = "No se encontró el registro solicitado."
RATING_NOT_FOUND_MESSAGE = "No se encontró el rating solicitado."
DUPLICATE_RATING_MESSAGE = "Este juego ya tiene un rating registrado."
CREATE_ERROR_MESSAGE = "No se pudo crear el rating del registro."
UPDATE_ERROR_MESSAGE = "No se pudo actualizar el rating del registro."
DELETE_ERROR_MESSAGE = "No se pudo eliminar el rating del registro."


class RatingService:
    def __init__(self, session: Session):
        self.session = session
        self.rating_repository = RatingRepository(session)
        self.archive_repository = ArchiveEntryRepository(session)
        self.activity_service = ActivityLogService(session)

    def get_rating_by_series_id(self, series_id: int) -> RatingRead:
        self._get_series_or_404(series_id)

        rating = self.rating_repository.get_by_series_id(series_id)
        if rating is None:
            raise self._rating_not_found_error()

        return map_rating_read(rating)

    def create_rating(self, series_id: int, payload: RatingCreate) -> RatingRead:
        entry = self._get_series_or_404(series_id)

        existing_rating = self.rating_repository.get_by_series_id(series_id)
        if existing_rating is not None:
            raise HTTPException(status_code=409, detail=DUPLICATE_RATING_MESSAGE)

        data = payload.model_dump(exclude_none=True)
        data["series_id"] = series_id

        try:
            rating = self.rating_repository.create(data)
            display_score = format_rating_score(float(rating.score))
            self.activity_service.record_activity(
                series_id=series_id,
                action="rating_created",
                message=f"Se registró un rating de {display_score} para '{entry.title}'.",
                previous_value=None,
                new_value=display_score,
            )
            self.session.commit()
            self.session.refresh(rating)
        except Exception as exc:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=CREATE_ERROR_MESSAGE) from exc

        return map_rating_read(rating)

    def update_rating(self, series_id: int, payload: RatingUpdate) -> RatingRead:
        entry = self._get_series_or_404(series_id)

        rating = self.rating_repository.get_by_series_id(series_id)
        if rating is None:
            raise self._rating_not_found_error()
        previous_score = format_rating_score(float(rating.score))

        data = payload.model_dump(exclude_unset=True)
        data["updated_at"] = datetime.now(timezone.utc)

        try:
            updated_rating = self.rating_repository.update(rating.id, data)
            if updated_rating is None:
                raise self._rating_not_found_error()
            new_score = format_rating_score(float(updated_rating.score))
            message = f"Se actualizó el rating de '{entry.title}' a {new_score}."
            self.activity_service.record_activity(
                series_id=series_id,
                action="rating_updated",
                message=message,
                previous_value=previous_score,
                new_value=new_score,
            )
            self.session.commit()
            self.session.refresh(updated_rating)
        except HTTPException:
            self.session.rollback()
            raise
        except Exception as exc:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=UPDATE_ERROR_MESSAGE) from exc

        return map_rating_read(updated_rating)

    def delete_rating(self, series_id: int) -> None:
        entry = self._get_series_or_404(series_id)

        rating = self.rating_repository.get_by_series_id(series_id)
        if rating is None:
            raise self._rating_not_found_error()
        previous_score = format_rating_score(float(rating.score))

        try:
            self.activity_service.record_activity(
                series_id=series_id,
                action="rating_deleted",
                message=f"Se eliminó el rating de '{entry.title}'.",
                previous_value=previous_score,
                new_value=None,
            )
            deleted = self.rating_repository.delete(rating.id)
            if not deleted:
                raise self._rating_not_found_error()
            self.session.commit()
        except HTTPException:
            self.session.rollback()
            raise
        except Exception as exc:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=DELETE_ERROR_MESSAGE) from exc

    def _ensure_series_exists(self, series_id: int) -> None:
        if not self.archive_repository.exists(series_id):
            raise HTTPException(status_code=404, detail=ENTRY_NOT_FOUND_MESSAGE)

    def _get_series_or_404(self, series_id: int):
        entry = self.archive_repository.get_by_id(series_id)
        if entry is None:
            raise HTTPException(status_code=404, detail=ENTRY_NOT_FOUND_MESSAGE)

        return entry

    def _rating_not_found_error(self) -> HTTPException:
        return HTTPException(status_code=404, detail=RATING_NOT_FOUND_MESSAGE)
