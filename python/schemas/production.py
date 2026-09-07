from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from python.schemas.script import ScriptPlan
from python.schemas.visual import VisualStoryboard
from python.schemas.gates import QualityGateReport

class PublishingPackage(BaseModel):
    primary_title: str
    alternate_titles: List[str] = []
    description: str
    hashtags: List[str] = []
    tags: List[str] = []
    category_id: str = '28' # Science & Technology
    language: str = 'en'
    contains_synthetic_media: bool = True

class ProductionCreate(BaseModel):
    channel_id: str
    topic_id: Optional[str] = None
    custom_topic: Optional[str] = None
    format: str = 'shorts' # shorts or long_form

class ProductionResponse(BaseModel):
    id: str
    channel_id: str
    topic_id: Optional[str]
    status: str
    format: str
    script_json: Dict[str, Any] = {}
    visual_json: Dict[str, Any] = {}
    publishing_json: Dict[str, Any] = {}
    review_json: Dict[str, Any] = {}
    final_video_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    audio_path: Optional[str] = None
    caption_path: Optional[str] = None
    video_hash_sha256: Optional[str] = None
    render_duration_seconds: float = 0.0
    estimated_cost_usd: float = 0.0
    created_at: datetime
    updated_at: datetime
