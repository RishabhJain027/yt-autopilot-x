from python.schemas.script import ScriptPlan
from python.schemas.visual import VisualStoryboard, ScenePlan

class VisualPlanner:
    def plan_visuals(self, script: ScriptPlan, aspect_ratio: str = '9:16') -> VisualStoryboard:
        scenes = []
        cinematic_styles = [
            "Hyperrealistic 3D octane render, glowing cybernetic neural network pulsing with neon cyan and magenta light, cinematic dolly zoom, 4k ultra-detailed, 60fps",
            "Futuristic holographic HUD interface assembling complex automated AI code in mid-air, dynamic camera panning, volumetric studio lighting, deep obsidian background",
            "Cinematic time-lapse of glowing data streams flowing across modern cityscape skyline, neon reflections, hyper-speed camera motion, photorealistic reflections",
            "High-energy macro shot of microscopic AI microchip core firing golden electrical sparks, extreme close-up, dramatic rim lighting, cinematic depth of field",
            "Sleek futuristic minimalist studio with floating glowing 3D efficiency charts and graphs rising upwards, clean modern aesthetics, smooth orbital camera rotation"
        ]

        for idx, seg in enumerate(script.segments):
            style = cinematic_styles[idx % len(cinematic_styles)]
            base_prompt = seg.visual_intent or f"Visual demonstration of: {seg.voiceover[:50]}"
            t2v_prompt = f"{base_prompt}. {style}"

            scenes.append(ScenePlan(
                scene_id=f"scene_{idx+1:03d}",
                duration=seg.duration,
                visual_type="t2v_remote_model",
                prompt=t2v_prompt,
                aspect_ratio=aspect_ratio,
                rights_status="generated_remote_t2v"
            ))

        return VisualStoryboard(aspect_ratio=aspect_ratio, scenes=scenes)

visual_planner = VisualPlanner()
