from datetime import datetime
from pydantic import BaseModel
from app.db.models import VideoStatus


class VideoCreateRequest(BaseModel):
    title: str
    description: str | None = None
    is_premium: bool = False
    input_url: str


class VideoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    is_premium: bool
    mux_asset_id: str | None
    playback_id: str | None
    status: VideoStatus
    created_by: int
    created_at: datetime


class PlayResponse(BaseModel):
    status: str
    playback_url: str | None = None
