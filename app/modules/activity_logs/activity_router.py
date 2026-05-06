from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.database import get_session
from app.modules.activity_logs.activity_schemas import (
    ActivityLogListResponse,
    ActivityLogQueryParams,
)
from app.modules.activity_logs.activity_service import ActivityLogService

router = APIRouter(prefix="/activity", tags=["Activity Logs"])
series_activity_router = APIRouter(prefix="/series", tags=["Activity Logs"])


def get_activity_log_service(
    session: Annotated[Session, Depends(get_session)],
) -> ActivityLogService:
    return ActivityLogService(session)


@router.get("", response_model=ActivityLogListResponse, status_code=status.HTTP_200_OK)
def list_recent_activity(
    query_params: Annotated[ActivityLogQueryParams, Depends()],
    service: Annotated[ActivityLogService, Depends(get_activity_log_service)],
) -> ActivityLogListResponse:
    return service.list_recent_activity(limit=query_params.limit)


@series_activity_router.get(
    "/{id}/activity",
    response_model=ActivityLogListResponse,
    status_code=status.HTTP_200_OK,
)
def list_activity_by_series_id(
    id: int,
    query_params: Annotated[ActivityLogQueryParams, Depends()],
    service: Annotated[ActivityLogService, Depends(get_activity_log_service)],
) -> ActivityLogListResponse:
    return service.list_activity_by_series_id(id, limit=query_params.limit)
