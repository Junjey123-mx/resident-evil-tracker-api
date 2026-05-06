from datetime import datetime, timezone

from fastapi import HTTPException
from sqlmodel import Session

# Registers the relationship target for standalone service/database usage.
from app.modules.activity_logs.activity_model import ActivityLog
from app.modules.archive_entries.archive_entry_mapper import (
    map_archive_entry_detail,
    map_archive_entry_list_response,
)
from app.modules.archive_entries.archive_entry_repository import ArchiveEntryRepository
from app.modules.archive_entries.archive_entry_schemas import (
    ArchiveEntryCreate,
    ArchiveEntryDetail,
    ArchiveEntryListResponse,
    ArchiveEntryQueryParams,
    ArchiveEntryUpdate,
)
from app.modules.personal_ratings.rating_repository import RatingRepository


NOT_FOUND_MESSAGE = "No se encontró el registro solicitado."
CREATE_ERROR_MESSAGE = "No se pudo crear el registro del archivo."
UPDATE_ERROR_MESSAGE = "No se pudo actualizar el registro del archivo."
DELETE_ERROR_MESSAGE = "No se pudo eliminar el registro del archivo."

_DEFAULT_CREATE_VALUES = {
    "category": "main_series",
    "status": "registered",
    "threat_level": "medium",
}


class ArchiveEntryService:
    def __init__(self, session: Session):
        self.session = session
        self.archive_repository = ArchiveEntryRepository(session)
        self.rating_repository = RatingRepository(session)

    def list_archive_entries(
        self,
        query_params: ArchiveEntryQueryParams,
    ) -> ArchiveEntryListResponse:
        if query_params.q or query_params.sort == "rating":
            entries = self.archive_repository.list_all()
            entries = self._filter_entries(entries, query_params.q)
            rating_scores = self._get_rating_scores(entries)
            entries = self._sort_entries(
                entries,
                query_params.sort,
                query_params.order,
                rating_scores,
            )
            total = len(entries)
            paginated_entries = self._paginate_entries(
                entries,
                query_params.page,
                query_params.limit,
            )
            paginated_scores = self._select_rating_scores(
                paginated_entries,
                rating_scores,
            )
            return map_archive_entry_list_response(
                paginated_entries,
                total=total,
                page=query_params.page,
                limit=query_params.limit,
                rating_scores=paginated_scores,
            )

        offset = (query_params.page - 1) * query_params.limit
        entries = self.archive_repository.list_paginated(
            offset=offset,
            limit=query_params.limit,
            sort_by=query_params.sort,
            sort_order=query_params.order,
        )
        total = self.archive_repository.count()
        rating_scores = self._get_rating_scores(entries)

        return map_archive_entry_list_response(
            entries,
            total=total,
            page=query_params.page,
            limit=query_params.limit,
            rating_scores=rating_scores,
        )

    def get_archive_entry_detail(self, entry_id: int) -> ArchiveEntryDetail:
        entry = self.archive_repository.get_by_id(entry_id)
        if entry is None:
            raise self._not_found_error()

        rating = self.rating_repository.get_by_series_id(entry_id)
        return map_archive_entry_detail(
            entry,
            rating_score=self._get_rating_score(rating),
            personal_review=self._get_rating_review(rating),
        )

    def create_archive_entry(self, payload: ArchiveEntryCreate) -> ArchiveEntryDetail:
        data = self._prepare_create_data(payload)

        try:
            entry = self.archive_repository.create(data)
            self.session.commit()
            self.session.refresh(entry)
        except Exception as exc:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=CREATE_ERROR_MESSAGE) from exc

        return map_archive_entry_detail(entry)

    def update_archive_entry(
        self,
        entry_id: int,
        payload: ArchiveEntryUpdate,
    ) -> ArchiveEntryDetail:
        entry = self.archive_repository.get_by_id(entry_id)
        if entry is None:
            raise self._not_found_error()

        data = self._prepare_update_data(payload)

        try:
            updated_entry = self.archive_repository.update(entry_id, data)
            if updated_entry is None:
                raise self._not_found_error()
            self.session.commit()
            self.session.refresh(updated_entry)
        except HTTPException:
            self.session.rollback()
            raise
        except Exception as exc:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=UPDATE_ERROR_MESSAGE) from exc

        rating = self.rating_repository.get_by_series_id(entry_id)
        return map_archive_entry_detail(
            updated_entry,
            rating_score=self._get_rating_score(rating),
            personal_review=self._get_rating_review(rating),
        )

    def delete_archive_entry(self, entry_id: int) -> None:
        entry = self.archive_repository.get_by_id(entry_id)
        if entry is None:
            raise self._not_found_error()

        try:
            deleted = self.archive_repository.delete(entry_id)
            if not deleted:
                raise self._not_found_error()
            self.session.commit()
        except HTTPException:
            self.session.rollback()
            raise
        except Exception as exc:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=DELETE_ERROR_MESSAGE) from exc

    def _prepare_create_data(self, payload: ArchiveEntryCreate) -> dict:
        data = payload.model_dump(exclude_none=True)
        for key, value in _DEFAULT_CREATE_VALUES.items():
            data.setdefault(key, value)
        return self._remap_engine_field(data)

    def _prepare_update_data(self, payload: ArchiveEntryUpdate) -> dict:
        data = payload.model_dump(exclude_unset=True, exclude_none=True)
        data["updated_at"] = datetime.now(timezone.utc)
        return self._remap_engine_field(data)

    def _remap_engine_field(self, data: dict) -> dict:
        if "engine" not in data:
            return data

        remapped = data.copy()
        remapped["engine_name"] = remapped.pop("engine")
        return remapped

    def _filter_entries(self, entries: list, query: str | None) -> list:
        if not query:
            return entries

        normalized_query = query.strip().lower()
        if not normalized_query:
            return entries

        return [
            entry
            for entry in entries
            if normalized_query in self._entry_search_text(entry)
        ]

    def _entry_search_text(self, entry) -> str:
        values = [
            getattr(entry, "title", None),
            getattr(entry, "alias_title", None),
            getattr(entry, "main_protagonist", None),
            getattr(entry, "original_platform", None),
            getattr(entry, "description", None),
        ]
        return " ".join(str(value).lower() for value in values if value)

    def _sort_entries(
        self,
        entries: list,
        sort: str,
        order: str,
        rating_scores: dict[int, float],
    ) -> list:
        reverse = order == "desc"

        if sort == "rating":
            return sorted(
                entries,
                key=lambda entry: rating_scores.get(self._get_entry_id(entry), -1),
                reverse=reverse,
            )

        return sorted(
            entries,
            key=lambda entry: getattr(entry, sort, None) or "",
            reverse=reverse,
        )

    def _paginate_entries(self, entries: list, page: int, limit: int) -> list:
        safe_limit = max(limit, 1)
        offset = (page - 1) * safe_limit
        return entries[offset : offset + safe_limit]

    def _get_rating_scores(self, entries: list) -> dict[int, float]:
        scores = {}
        for entry in entries:
            entry_id = self._get_entry_id(entry)
            rating = self.rating_repository.get_by_series_id(entry_id)
            score = self._get_rating_score(rating)
            if score is not None:
                scores[entry_id] = score
        return scores

    def _select_rating_scores(
        self,
        entries: list,
        rating_scores: dict[int, float],
    ) -> dict[int, float]:
        entry_ids = {self._get_entry_id(entry) for entry in entries}
        return {
            entry_id: score
            for entry_id, score in rating_scores.items()
            if entry_id in entry_ids
        }

    def _get_rating_score(self, rating) -> float | None:
        if rating is None or rating.score is None:
            return None

        return float(rating.score)

    def _get_rating_review(self, rating) -> str | None:
        if rating is None:
            return None

        return rating.review

    def _get_entry_id(self, entry) -> int:
        entry_id = getattr(entry, "id", 0)
        return entry_id or 0

    def _not_found_error(self) -> HTTPException:
        return HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)
