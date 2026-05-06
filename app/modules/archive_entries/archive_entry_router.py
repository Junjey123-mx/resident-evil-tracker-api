from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session

from app.db.database import get_session
from app.modules.archive_entries.archive_entry_schemas import (
    ArchiveEntryCreate,
    ArchiveEntryDetail,
    ArchiveEntryListResponse,
    ArchiveEntryQueryParams,
    ArchiveEntryUpdate,
)
from app.modules.archive_entries.archive_entry_service import ArchiveEntryService

router = APIRouter(prefix="/series", tags=["Archive Entries"])


def get_archive_entry_service(
    session: Annotated[Session, Depends(get_session)],
) -> ArchiveEntryService:
    return ArchiveEntryService(session)


@router.get("", response_model=ArchiveEntryListResponse, status_code=status.HTTP_200_OK)
def list_archive_entries(
    query_params: Annotated[ArchiveEntryQueryParams, Depends()],
    service: Annotated[ArchiveEntryService, Depends(get_archive_entry_service)],
) -> ArchiveEntryListResponse:
    return service.list_archive_entries(query_params)


@router.get("/{id}", response_model=ArchiveEntryDetail, status_code=status.HTTP_200_OK)
def get_archive_entry_detail(
    id: int,
    service: Annotated[ArchiveEntryService, Depends(get_archive_entry_service)],
) -> ArchiveEntryDetail:
    return service.get_archive_entry_detail(id)


@router.post(
    "",
    response_model=ArchiveEntryDetail,
    status_code=status.HTTP_201_CREATED,
)
def create_archive_entry(
    payload: ArchiveEntryCreate,
    service: Annotated[ArchiveEntryService, Depends(get_archive_entry_service)],
) -> ArchiveEntryDetail:
    return service.create_archive_entry(payload)


@router.put("/{id}", response_model=ArchiveEntryDetail, status_code=status.HTTP_200_OK)
def update_archive_entry(
    id: int,
    payload: ArchiveEntryUpdate,
    service: Annotated[ArchiveEntryService, Depends(get_archive_entry_service)],
) -> ArchiveEntryDetail:
    return service.update_archive_entry(id, payload)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_archive_entry(
    id: int,
    service: Annotated[ArchiveEntryService, Depends(get_archive_entry_service)],
) -> Response:
    service.delete_archive_entry(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
