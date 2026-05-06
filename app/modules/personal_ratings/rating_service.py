from datetime import datetime, timezone

from fastapi import HTTPException
from sqlmodel import Session

# Registers ArchiveEntry relationship targets for standalone service/database usage.
from app.modules.activity_logs.activity_model import ActivityLog
from app.modules.archive_entries.archive_entry_repository import ArchiveEntryRepository
from app.modules.personal_ratings.rating_mapper import map_rating_read
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

    def get_rating_by_series_id(self, series_id: int) -> RatingRead:
        self._ensure_series_exists(series_id)

        rating = self.rating_repository.get_by_series_id(series_id)
        if rating is None:
            raise self._rating_not_found_error()

        return map_rating_read(rating)

    def create_rating(self, series_id: int, payload: RatingCreate) -> RatingRead:
        self._ensure_series_exists(series_id)

        existing_rating = self.rating_repository.get_by_series_id(series_id)
        if existing_rating is not None:
            raise HTTPException(status_code=409, detail=DUPLICATE_RATING_MESSAGE)

        data = payload.model_dump(exclude_none=True)
        data["series_id"] = series_id

        try:
            rating = self.rating_repository.create(data)
            self.session.commit()
            self.session.refresh(rating)
        except Exception as exc:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=CREATE_ERROR_MESSAGE) from exc

        return map_rating_read(rating)

    def update_rating(self, series_id: int, payload: RatingUpdate) -> RatingRead:
        self._ensure_series_exists(series_id)

        rating = self.rating_repository.get_by_series_id(series_id)
        if rating is None:
            raise self._rating_not_found_error()

        data = payload.model_dump(exclude_unset=True)
        data["updated_at"] = datetime.now(timezone.utc)

        try:
            updated_rating = self.rating_repository.update(rating.id, data)
            if updated_rating is None:
                raise self._rating_not_found_error()
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
        self._ensure_series_exists(series_id)

        rating = self.rating_repository.get_by_series_id(series_id)
        if rating is None:
            raise self._rating_not_found_error()

        try:
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

    def _rating_not_found_error(self) -> HTTPException:
        return HTTPException(status_code=404, detail=RATING_NOT_FOUND_MESSAGE)
