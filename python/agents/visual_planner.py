"""
Visual Planner Agent for Maya ✨ Cutie Baddie.
Plans photorealistic, high-aesthetic visual storyboards for Text-to-Video synthesis across
remote cloud models (Wan 2.2, HunyuanVideo 1.5, LTX-2.5, MiniMax-H3, AnimateDiff-Lightning).
Embodies Maya ✨ (21yo gorgeous, cute, clumsy aesthetic girl, Portra 400 35mm film still,
warm golden hour Parisian/NYC cafe, soft lighting, depth of field, clean frames with strictly NO text boxes).
"""

from typing import Optional
from python.schemas.script import ScriptPlan
from python.schemas.visual import VisualStoryboard, ScenePlan
from packages.logger.logger import logger

class VisualPlanner:
    def plan_visuals(self, script: ScriptPlan, aspect_ratio: str = '9:16', niche: Optional[str] = None) -> VisualStoryboard:
        logger.info(f"[VISUAL_PLANNER] Planning {len(script.segments)} visual scenes for Maya ✨ in {aspect_ratio} format...")

        # Consistent AI Character Prompts: Maya (21yo gorgeous, cute, clumsy aesthetic girl)
        aesthetic_enhancers = [
            "Maya 21yo stylish cute clumsy aesthetic girl with messy brunette hair bun and curtain bangs, oversized cream knit sweater, sunlit minimalist aesthetic loft, holding iced latte, candid Kodak Portra 400 35mm film photography, soft natural golden hour glow, shallow depth of field, photorealistic 8k, ultra-detailed skin texture, clean frame, NO text boxes",
            "Maya sitting at cozy Parisian café terrace outdoor table, chic vintage sunglasses pushed on head, cute oversized beige trench coat, laughing candidly, authentic film grain, soft cinematic lighting, 8k photorealistic portrait, clean composition, NO text boxes",
            "Maya in a dreamy aesthetic room with soft ambient pastel lighting, floating fairy lights, looking into camera with alluring warm smile, cinematic 35mm film still, high fashion editorial vibe, photorealistic, NO text boxes",
            "Maya walking gracefully down modern aesthetic city street during sunset, warm ambient bokeh, stylish baggy streetwear, candid lifestyle photograph, smooth tracking camera glide, photorealistic, NO text boxes",
            "Maya in a cozy aesthetic vinyl record shop, soft warm indoor lighting, playful expressive wink at camera, holding retro pastel headphones, cinematic 35mm film still, depth of field, 8k resolution, NO text boxes"
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
