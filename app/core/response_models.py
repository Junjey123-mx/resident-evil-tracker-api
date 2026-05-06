from typing import Optional

from pydantic import BaseModel


class APIMessageResponse(BaseModel):
    message: str


class APIErrorResponse(BaseModel):
    error: str
    message: str
    field: Optional[str] = None
    status_code: int


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str
    version: str
