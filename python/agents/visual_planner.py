"""
Visual Planner Agent.
Plans photorealistic, high-energy visual storyboards for Text-to-Video synthesis across
remote cloud models (Wan2.1-T2V-1.3B, CogVideoX, LTX-Video, Cloud Flux).
"""

from python.schemas.script import ScriptPlan
from python.schemas.visual import VisualStoryboard, ScenePlan
from packages.logger.logger import logger

class VisualPlanner:
    def plan_visuals(self, script: ScriptPlan, aspect_ratio: str = '9:16') -> VisualStoryboard:
        logger.info(f"[VISUAL_PLANNER] Planning {len(script.segments)} visual scenes in {aspect_ratio} format...")
        
        scenes = []
        cinematic_enhancers = [
            "Hyperrealistic 3D octane render, glowing cybernetic neural network pulsing with neon cyan and magenta energy, cinematic lighting, 8k resolution, ultra-detailed, Unreal Engine 5 render",
            "Futuristic holographic HUD interface assembling complex automated AI code in mid-air, dynamic camera panning, volumetric studio lighting, deep obsidian background, high tech aesthetic",
            "Cinematic time-lapse of glowing data streams flowing across modern cityscape skyline, neon reflections, hyper-speed camera motion, photorealistic reflections, 4k",
            "High-energy macro shot of microscopic AI microchip core firing golden electrical sparks, extreme close-up, dramatic rim lighting, cinematic depth of field",
            "Sleek futuristic minimalist studio with floating glowing 3D efficiency charts and graphs rising upwards, clean modern aesthetics, smooth orbital camera rotation"
        ]

        for idx, seg in enumerate(script.segments):
            enhancer = cinematic_enhancers[idx % len(cinematic_enhancers)]
            base_prompt = seg.visual_intent if seg.visual_intent else f"Cinematic visual representation of {seg.voiceover[:60]}"
            t2v_prompt = f"{base_prompt}. {enhancer}"

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
