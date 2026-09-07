from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class NicheScoreInput(BaseModel):
    language: str = 'en'
    target_region: str = 'global'
    faceless: bool = True
    shorts: bool = True
    long_form: bool = True
    budget: str = 'medium'
    risk_tolerance: str = 'low'

class NicheProposal(BaseModel):
    niche: str
    score: float
    audience: str
    primary_format: str = 'shorts'
    secondary_format: str = 'long_form'
    content_pillars: List[str]
    risk_notes: List[str] = []
    evidence: List[Dict[str, Any]] = []

class TopicCandidate(BaseModel):
    id: Optional[str] = None
    topic: str
    score: float = 0.0
    trend_score: float = 0.0
    competition_score: float = 0.0
    rights_risk: float = 0.0
    channel_fit: float = 0.9
    momentum: float = 0.8
    source: str = 'trend_radar'
    status: str = 'DISCOVERED'
    evidence: Dict[str, Any] = {}
