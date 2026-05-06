from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RatingCreate(BaseModel):
    score: float = Field(ge=1, le=10)
    review: Optional[str] = Field(default=None, max_length=500)


class RatingUpdate(BaseModel):
    score: Optional[float] = Field(default=None, ge=1, le=10)
    review: Optional[str] = Field(default=None, max_length=500)


class RatingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    series_id: int
    score: float
    display_score: str
    review: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class RatingMessageResponse(BaseModel):
    message: str
