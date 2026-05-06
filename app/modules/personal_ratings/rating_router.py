from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session

from app.db.database import get_session
from app.modules.personal_ratings.rating_schemas import (
    RatingCreate,
    RatingRead,
    RatingUpdate,
)
from app.modules.personal_ratings.rating_service import RatingService

router = APIRouter(prefix="/series", tags=["Personal Ratings"])


def get_rating_service(
    session: Annotated[Session, Depends(get_session)],
) -> RatingService:
    return RatingService(session)


@router.get("/{id}/rating", response_model=RatingRead, status_code=status.HTTP_200_OK)
def get_rating_by_series_id(
    id: int,
    service: Annotated[RatingService, Depends(get_rating_service)],
) -> RatingRead:
    return service.get_rating_by_series_id(id)


@router.post(
    "/{id}/rating",
    response_model=RatingRead,
    status_code=status.HTTP_201_CREATED,
)
def create_rating(
    id: int,
    payload: RatingCreate,
    service: Annotated[RatingService, Depends(get_rating_service)],
) -> RatingRead:
    return service.create_rating(id, payload)


@router.put("/{id}/rating", response_model=RatingRead, status_code=status.HTTP_200_OK)
def update_rating(
    id: int,
    payload: RatingUpdate,
    service: Annotated[RatingService, Depends(get_rating_service)],
) -> RatingRead:
    return service.update_rating(id, payload)


@router.delete("/{id}/rating", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(
    id: int,
    service: Annotated[RatingService, Depends(get_rating_service)],
) -> Response:
    service.delete_rating(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
