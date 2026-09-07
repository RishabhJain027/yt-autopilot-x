from python.schemas.script import ScriptPlan
from python.schemas.visual import VisualStoryboard, ScenePlan

class VisualPlanner:
    def plan_visuals(self, script: ScriptPlan, aspect_ratio: str = '9:16') -> VisualStoryboard:
        scenes = []
        for idx, seg in enumerate(script.segments):
            scenes.append(ScenePlan(
                scene_id=f"scene_{idx+1:03d}",
                duration=seg.duration,
                visual_type="procedural",
                prompt=seg.visual_intent or f"Visual for: {seg.voiceover[:40]}",
                aspect_ratio=aspect_ratio,
                rights_status="generated"
            ))
        return VisualStoryboard(aspect_ratio=aspect_ratio, scenes=scenes)

visual_planner = VisualPlanner()
