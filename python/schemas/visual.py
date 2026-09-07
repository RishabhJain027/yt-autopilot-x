from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ScenePlan(BaseModel):
    scene_id: str
    duration: float
    visual_type: str = 'procedural' # procedural, ai_video, stock, original, motion_graphic
    prompt: str
    aspect_ratio: str = '9:16' # 9:16 for shorts, 16:9 for long_form
    rights_status: str = 'generated'
    local_path: Optional[str] = None

class VisualStoryboard(BaseModel):
    aspect_ratio: str = '9:16'
    scenes: List[ScenePlan]
    background_music_track: Optional[str] = None
    color_scheme: List[str] = ['#1E1E2E', '#FF0055']
