"""
Visual Planner Agent for Maya ✨ Cutie Baddie.
Plans hyper-gorgeous, photorealistic, high-aesthetic visual storyboards for Text-to-Video synthesis across
remote flagship open-source models (Wan 2.2 14B MoE, HunyuanVideo 1.5 13B, MiniMax-H3 14B MoE).
Embodies Maya ✨ (21yo stunning gorgeous aesthetic baddie, captivating hazel eyes, dreamy lips,
messy bun, golden hour loft, chic Parisian cafe, luxury silk robe, Portra 400 35mm film still,
strictly clean frames with NO on-screen text or subtitles).
"""

from typing import Optional
from python.schemas.script import ScriptPlan
from python.schemas.visual import VisualStoryboard, ScenePlan
from packages.logger.logger import logger

class VisualPlanner:
    def plan_visuals(self, script: ScriptPlan, aspect_ratio: str = '9:16', niche: Optional[str] = None) -> VisualStoryboard:
        logger.info(f"[VISUAL_PLANNER] Planning {len(script.segments)} hyper-gorgeous visual scenes for Maya ✨ in {aspect_ratio} format...")

        # Consistent Flagship AI Character Prompts: Maya (21yo stunning gorgeous aesthetic baddie)
        aesthetic_enhancers = [
            "Maya 21yo stunning gorgeous aesthetic baddie, captivating hazel eyes, dreamy lips, messy brunette bun with face-framing strands, luxury cream silk slip dress, sunlit golden hour loft, soft natural glow, Kodak Portra 400 35mm film still, depth of field, photorealistic 8k, ultra-detailed skin texture, clean frame, NO text, NO subtitles",
            "Maya sitting at chic Parisian cafe terrace outdoor table, chic vintage sunglasses pushed on head, oversized beige trench coat, sipping iced matcha latte, glancing seductively into camera with playful smile, warm ambient lighting, 35mm film grain, 8k cinematic portrait, clean frame, NO text boxes",
            "Maya in a dreamy aesthetic boudoir room with soft velvet cushions and floating fairy lights, looking intimately into camera with alluring warm gaze, high-fashion editorial aesthetic, 8k photorealistic, clean frame, NO text, NO subtitles",
            "Maya walking gracefully down glowing city avenue during sunset in stylish chic streetwear, warm golden hour bokeh, candid high-fashion lifestyle, cinematic tracking camera glide, clean frame, NO text, NO subtitles",
            "Maya applying luxury botanical perfume with alluring playful expression, playful expressive wink at camera in sunlit bedroom, cinematic 35mm film still, depth of field, 8k resolution, clean frame, NO text, NO subtitles"
        ]

        scenes = []
        for idx, seg in enumerate(script.segments):
            enhancer = aesthetic_enhancers[idx % len(aesthetic_enhancers)]
            base_prompt = seg.visual_intent if seg.visual_intent else f"Aesthetic visual scene of {seg.voiceover[:60]}"
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
