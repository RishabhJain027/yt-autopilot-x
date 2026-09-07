from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class AnalyticsSnapshotSchema(BaseModel):
    youtube_video_id: str
    views: int = 0
    likes: int = 0
    comments: int = 0
    watch_time_minutes: float = 0.0
    average_view_duration_seconds: float = 0.0
    ctr: float = 0.0
    retention_curve: Dict[str, float] = {}

class LearningRecommendationSchema(BaseModel):
    id: Optional[str] = None
    channel_id: str
    finding: str
    evidence_count: int
    confidence: float
    metric: str
    recommended_action: str
    status: str = 'PENDING_APPROVAL'
