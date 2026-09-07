from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class BrandKit(BaseModel):
    name: str = 'YT Automation Channel'
    tagline: str = ''
    tone: List[str] = ['smart', 'practical', 'energetic']
    primary_color: str = '#FF0000'
    secondary_color: str = '#1E1E2E'
    font_heading: str = 'Inter'
    font_body: str = 'Roboto'
    logo_style: str = 'minimal geometric'
    thumbnail_style: str = 'high contrast, one focal object, 3-5 words max'

class AudienceProfile(BaseModel):
    target_demographic: str = '18-34 tech/productivity learners'
    interests: List[str] = ['AI tools', 'software', 'productivity', 'workflows']
    geography: str = 'global'
    preferred_format: str = 'shorts'

class ChannelCreate(BaseModel):
    youtube_channel_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    google_account_email: Optional[str] = None
    niche: Optional[str] = None
    language_code: str = 'en'
    timezone: str = 'Asia/Kolkata'
    operating_mode: str = 'APPROVAL_FIRST'

class ChannelResponse(BaseModel):
    id: str
    youtube_channel_id: str
    title: Optional[str]
    description: Optional[str]
    niche: Optional[str]
    language_code: str
    timezone: str
    operating_mode: str
    status: str
    created_at: datetime
    updated_at: datetime
