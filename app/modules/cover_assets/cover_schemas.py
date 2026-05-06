from typing import Optional

from pydantic import BaseModel


class CoverUploadResponse(BaseModel):
    series_id: int
    cover_image_url: str
    cover_image_public_id: str
    message: str
    action: Optional[str] = None
