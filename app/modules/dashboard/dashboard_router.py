from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.database import get_session
from app.modules.dashboard.dashboard_schemas import DashboardStatsResponse
from app.modules.dashboard.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_dashboard_service(
    session: Annotated[Session, Depends(get_session)],
) -> DashboardService:
    return DashboardService(session)


@router.get(
    "/stats",
    response_model=DashboardStatsResponse,
    status_code=status.HTTP_200_OK,
)
def get_dashboard_stats(
    service: Annotated[DashboardService, Depends(get_dashboard_service)],
) -> DashboardStatsResponse:
    return service.get_dashboard_stats()
