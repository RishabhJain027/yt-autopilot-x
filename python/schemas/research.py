from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ClaimItem(BaseModel):
    claim_id: str
    claim_text: str
    source_url: Optional[str] = None
    source_title: Optional[str] = None
    source_publisher: Optional[str] = None
    retrieved_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    confidence: float = 1.0
    supports_claim: bool = True
    requires_human_review: bool = False

class SourceAttribution(BaseModel):
    url: str
    publisher: str
    title: Optional[str] = None
    retrieved_at: str
    claims_supported: List[str] = []

class ResearchPacket(BaseModel):
    topic: str
    facts: List[str] = []
    claims: List[ClaimItem] = []
    sources: List[SourceAttribution] = []
    contradictions: List[str] = []
    uncertainties: List[str] = []
    claims_requiring_human_review: List[str] = []
