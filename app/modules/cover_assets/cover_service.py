from fastapi import HTTPException, UploadFile
from sqlmodel import Session

from app.modules.activity_logs.activity_service import ActivityLogService
from app.modules.archive_entries.archive_entry_repository import ArchiveEntryRepository
from app.modules.cover_assets.cloudinary_gateway import (
    CloudinaryConfigurationError,
    CloudinaryGateway,
)
from app.modules.cover_assets.cover_schemas import CoverUploadResponse


ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_COVER_SIZE_BYTES = 1024 * 1024
NOT_FOUND_MESSAGE = "No se encontró el registro solicitado."
INVALID_TYPE_MESSAGE = "Tipo de archivo no permitido."
OVERSIZED_FILE_MESSAGE = "La portada no debe superar 1 MB."
CLOUDINARY_ERROR_MESSAGE = "Cloudinary no está configurado."
UPLOAD_ERROR_MESSAGE = "No se pudo subir la portada."


class CoverService:
    def __init__(self, session: Session):
        self.session = session
        self.archive_repository = ArchiveEntryRepository(session)
        self.activity_service = ActivityLogService(session)
        self.cloudinary_gateway = CloudinaryGateway()

    def upload_cover(self, series_id: int, file: UploadFile) -> CoverUploadResponse:
        entry = self.archive_repository.get_by_id(series_id)
        if entry is None:
            raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)

        self._validate_content_type(file.content_type)
        file_content = self._read_file_content(file)
        had_cover = bool(entry.cover_image_url)
        previous_public_id = entry.cover_image_public_id

        try:
            upload_result = self.cloudinary_gateway.upload_cover(
                file_content=file_content,
                filename=file.filename or f"series-{series_id}-cover",
                content_type=file.content_type or "",
            )
            cover_image_url = upload_result.get("secure_url")
            cover_image_public_id = upload_result.get("public_id")
            if not cover_image_url or not cover_image_public_id:
                raise HTTPException(status_code=502, detail=UPLOAD_ERROR_MESSAGE)

            updated_entry = self.archive_repository.update(
                series_id,
                {
                    "cover_image_url": cover_image_url,
                    "cover_image_public_id": cover_image_public_id,
                },
            )
            if updated_entry is None:
                raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)

            action = "cover_updated" if had_cover else "cover_uploaded"
            message = (
                f"Se actualizó la portada de '{updated_entry.title}'."
                if had_cover
                else f"Se subió una portada para '{updated_entry.title}'."
            )
            self.activity_service.record_activity(
                series_id=series_id,
                action=action,
                message=message,
                previous_value=previous_public_id if had_cover else None,
                new_value=cover_image_public_id,
            )
            self.session.commit()
            self.session.refresh(updated_entry)
        except CloudinaryConfigurationError as exc:
            self.session.rollback()
            raise HTTPException(status_code=503, detail=CLOUDINARY_ERROR_MESSAGE) from exc
        except HTTPException:
            self.session.rollback()
            raise
        except Exception as exc:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=UPLOAD_ERROR_MESSAGE) from exc

        return CoverUploadResponse(
            series_id=series_id,
            cover_image_url=updated_entry.cover_image_url,
            cover_image_public_id=updated_entry.cover_image_public_id,
            message=message,
            action=action,
        )

    def _validate_content_type(self, content_type: str | None) -> None:
        if content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(status_code=400, detail=INVALID_TYPE_MESSAGE)

    def _read_file_content(self, file: UploadFile) -> bytes:
        content = file.file.read(MAX_COVER_SIZE_BYTES + 1)
        if len(content) > MAX_COVER_SIZE_BYTES:
            raise HTTPException(status_code=400, detail=OVERSIZED_FILE_MESSAGE)

        return content
