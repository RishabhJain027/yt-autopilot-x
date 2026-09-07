from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ScriptSegment(BaseModel):
    id: str
    voiceover: str
    duration: float = 5.0
    visual_intent: str = ''
    claims: List[str] = []

class ScriptPlan(BaseModel):
    title_candidate: str
    hook: str
    context: str = ''
    core_value: str = ''
    proof: str = ''
    payoff: str = ''
    cta: str
    segments: List[ScriptSegment]
    format: str = 'shorts'
    estimated_duration_seconds: float = 45.0
