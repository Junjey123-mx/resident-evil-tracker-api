from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlmodel import Session

from app.db.database import get_session
from app.modules.cover_assets.cover_schemas import CoverUploadResponse
from app.modules.cover_assets.cover_service import CoverService

router = APIRouter(prefix="/series", tags=["Cover Assets"])


def get_cover_service(
    session: Annotated[Session, Depends(get_session)],
) -> CoverService:
    return CoverService(session)


@router.post(
    "/{id}/cover",
    response_model=CoverUploadResponse,
    status_code=status.HTTP_200_OK,
)
def upload_cover(
    id: int,
    file: Annotated[UploadFile, File(...)],
    service: Annotated[CoverService, Depends(get_cover_service)],
) -> CoverUploadResponse:
    return service.upload_cover(id, file)
