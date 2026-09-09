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

        # Consistent Flagship AI Character Prompts: Maya (21yo Wild Free-Spirited Gossip Girl Baddie with Crazy Magnetic Eyes)
        aesthetic_enhancers = [
            "Maya 21yo stunning wild free-spirited Upper East Side Gossip Girl baddie, captivating wide crazy wild electric hazel eyes with intense hypnotic siren gaze, bold magnetic direct eye contact into camera, gorgeous radiant smirk, voluminous wind-blown messy blowout, luxury champagne silk dress and delicate gold jewelry, Manhattan penthouse terrace overlooking skyline at golden hour, soft natural glow, Kodak Portra 400 35mm film still, depth of field, photorealistic 8k, ultra-detailed skin texture, clean frame, strictly NO text, NO subtitles",
            "Maya 21yo wild aesthetic baddie with mesmerizing intense open hazel eyes sparkling with untamed energy, sitting at chic Upper East Side cafe terrace outdoor table, pushing vintage sunglasses onto hair, gazing seductively and playfully straight into camera lens, wind blowing hair strands, warm ambient golden lighting, 35mm film grain, 8k cinematic portrait, clean frame, NO text boxes",
            "Maya 21yo free-spirited gorgeous baddie with wildly captivating electric siren eyes and carefree alluring smile, sitting on the Metropolitan Museum steps in Manhattan in high-fashion outfit, looking intimately and intensely into camera with unstoppable confidence, paparazzi flash editorial aesthetic, 8k photorealistic, clean frame, NO text, NO subtitles",
            "Maya 21yo radiant wild baddie walking effortlessly down 5th Avenue during glowing dusk in chic dress, turning head with crazy magnetic eye contact and playful teasing smile, hair blowing freely in the evening breeze, warm golden hour bokeh, candid high-fashion lifestyle, cinematic tracking camera glide, clean frame, NO text, NO subtitles",
            "Maya 21yo stunning baddie at vanity mirror, locking wide wild seductive eyes with camera in reflection, playful expressive wink and mesmerizing gaze in sunlit Manhattan penthouse boudoir, cinematic 35mm film still, depth of field, 8k resolution, clean frame, NO text, NO subtitles"
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

