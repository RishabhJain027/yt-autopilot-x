from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class UploadRequest(BaseModel):
    production_id: str
    privacy_status: str = 'private' # private, unlisted, public
    publish_at: Optional[datetime] = None
    contains_synthetic_media: bool = True

class ReconciliationReport(BaseModel):
    youtube_video_id: str
    local_status: str
    remote_status: str
    remote_privacy: str
    scheduled_time: Optional[str] = None
    reconciled_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    synchronized: bool
