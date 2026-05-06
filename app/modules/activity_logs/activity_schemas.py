from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ActivityLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    series_id: Optional[int] = None
    action: str
    action_label: str
    message: str
    previous_value: Optional[str] = None
    new_value: Optional[str] = None
    created_at: datetime
    display_date: Optional[str] = None


class ActivityLogListResponse(BaseModel):
    items: list[ActivityLogRead]
    total: int
    limit: int


class ActivityLogQueryParams(BaseModel):
    limit: int = Field(default=10, ge=1, le=50)
