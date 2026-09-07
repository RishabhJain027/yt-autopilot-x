from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class GateResult(BaseModel):
    passed: bool
    score: float = 1.0
    details: str = ''
    violations: List[str] = []

class QualityGateReport(BaseModel):
    factuality_gate: GateResult
    rights_gate: GateResult
    duplicate_gate: GateResult
    safety_gate: GateResult
    synthetic_media_gate: GateResult
    render_gate: GateResult
    overall_passed: bool
    requires_human_review: bool = False
    reason: Optional[str] = None
