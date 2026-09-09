"""
Visual Planner Agent.
Plans photorealistic, high-energy visual storyboards for Text-to-Video synthesis across
remote cloud models (Wan 2.2, Wan 2.1, HunyuanVideo 1.5, LTX-2.5, MiniMax-H3, Cosmos, Cloud Flux).
Supports photorealistic AI character visual consistency for Pinterest Aesthetic / Clumsy GenZ Hot Baddie & AI Lifestyle
and futuristic cinematic renders for Tech Breakthroughs. Strictly enforces clean rendering with NO ugly printed text boxes.
"""

from typing import Optional
from python.schemas.script import ScriptPlan
from python.schemas.visual import VisualStoryboard, ScenePlan
from packages.logger.logger import logger

class VisualPlanner:
    def plan_visuals(self, script: ScriptPlan, aspect_ratio: str = '9:16', niche: Optional[str] = None) -> VisualStoryboard:
        logger.info(f"[VISUAL_PLANNER] Planning {len(script.segments)} visual scenes in {aspect_ratio} format (Niche: {niche or 'auto'})...")

        # Detect niche from script content or parameter
        script_text = f"{script.title_candidate} {script.hook} {' '.join(s.voiceover for s in script.segments)}".lower()
        is_genz_aesthetic = any(k in script_text or (niche and k in niche.lower()) for k in [
            "pinterest", "aesthetic", "genz", "baddie", "girl", "lifestyle", "character", "clumsy", "matcha", "ootd", "sophia"
        ])

        scenes = []

        if is_genz_aesthetic:
            # Consistent AI Character Prompts: Sophia (22yo stylish clumsy GenZ lifestyle creator)
            aesthetic_enhancers = [
                "Sophia 22yo stylish clumsy GenZ girl with messy brunette hair bun, oversized neutral cream knit sweater, sunlit minimalist aesthetic loft kitchen, holding matcha cup, candid Kodak Portra 400 35mm film photography, soft natural golden hour glow, shallow depth of field, photorealistic 8k, ultra-detailed skin texture, clean frame, NO text boxes",
                "Sophia sitting at cozy Parisian café terrace outdoor table, chic vintage sunglasses pushed on head, cute oversized trench coat, laughing candidly, authentic film grain, soft cinematic lighting, 8k photorealistic portrait, clean composition, NO text boxes",
                "Sophia walking gracefully down modern aesthetic city street during sunset, warm ambient bokeh, stylish baggy streetwear, candid high-fashion lifestyle photograph, smooth tracking camera glide, photorealistic, NO text boxes",
                "Sophia in a cozy aesthetic vinyl record shop, soft warm indoor lighting, playful expressive smile, holding retro headphone, cinematic 35mm film still, depth of field, 8k resolution, NO text boxes",
                "Sophia in a modern bright bedroom vanity setup with floating fairy lights, elegant pastel aesthetic, candid playful wink at camera, soft studio lighting, ultra-sharp focus, NO text boxes"
            ]

            for idx, seg in enumerate(script.segments):
                enhancer = aesthetic_enhancers[idx % len(aesthetic_enhancers)]
                base_prompt = seg.visual_intent if seg.visual_intent else f"Aesthetic lifestyle scene of {seg.voiceover[:60]}"
                t2v_prompt = f"{base_prompt}. {enhancer}"

                scenes.append(ScenePlan(
                    scene_id=f"scene_{idx+1:03d}",
                    duration=seg.duration,
                    visual_type="t2v_remote_model",
                    prompt=t2v_prompt,
                    aspect_ratio=aspect_ratio,
                    rights_status="generated_remote_t2v"
                ))
        else:
            # High-Tech / AI Breakthroughs Visual Storyboard
            cinematic_enhancers = [
                "Hyperrealistic 3D octane render, glowing cybernetic neural network pulsing with neon cyan and magenta energy, volumetric studio lighting, 8k resolution, ultra-detailed, Unreal Engine 5 render, clean frame, NO text boxes",
                "Futuristic holographic HUD interface assembling complex automated AI code in mid-air, dynamic camera panning, volumetric studio lighting, deep obsidian background, high tech aesthetic, NO text boxes",
                "Cinematic time-lapse of glowing data streams flowing across modern cityscape skyline, neon reflections, hyper-speed camera motion, photorealistic reflections, 4k, NO text boxes",
                "High-energy macro shot of microscopic AI microchip core firing golden electrical sparks, extreme close-up, dramatic rim lighting, cinematic depth of field, NO text boxes",
                "Sleek futuristic minimalist studio with floating glowing 3D efficiency charts and graphs rising upwards, clean modern aesthetics, smooth orbital camera rotation, NO text boxes"
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

