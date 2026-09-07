from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class AssetProvenance(BaseModel):
    asset_id: str
    source_type: str = 'generated' # generated, licensed_stock, public_domain, creator_owned
    source_url: Optional[str] = None
    creator: Optional[str] = 'AI System'
    license_name: str = 'AI Generated Original'
    license_url: Optional[str] = None
    commercial_use: bool = True
    modification_allowed: bool = True
    attribution_required: bool = False
    retrieved_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    checksum_sha256: Optional[str] = None
    rights_status: str = 'VERIFIED' # UNKNOWN, PENDING, VERIFIED, REJECTED, EXPIRED
    rights_verified_by: str = 'machine_gate'
