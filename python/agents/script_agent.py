"""
Master YouTube Script Agent.
Generates fast-paced, retention-optimized viral video scripts with 5-part structure:
Hook (0-2s) -> Context (2-8s) -> Core Value/Storytime (8-25s) -> Proof/Benchmark (25-35s) -> Payoff & CTA (35-45s).
Supports both "AI Tools, Automation & Tech Breakthroughs" and "Pinterest Aesthetic / Clumsy GenZ Hot Baddie & AI Character Lifestyle".
"""

from typing import Dict, Any, List, Optional
from python.schemas.script import ScriptPlan, ScriptSegment
from python.schemas.research import ResearchPacket
from python.services.llm_service import llm_service
from packages.logger.logger import logger, audit_log

class ScriptAgent:
    async def generate_script(self, topic: str, research: ResearchPacket, format: str = 'shorts', niche: Optional[str] = None) -> ScriptPlan:
        logger.info(f"[SCRIPT_AGENT] Generating high-retention {format} script for topic: '{topic}' (Niche: {niche or 'auto'})...")

        # Detect if topic or niche is Pinterest / GenZ / Clumsy Baddie / AI Character
        topic_lower = topic.lower()
        niche_lower = (niche or '').lower()
        is_genz_aesthetic = any(k in topic_lower or k in niche_lower for k in [
            "pinterest", "aesthetic", "genz", "baddie", "girl", "lifestyle", "character", "clumsy", "pov", "matcha", "ootd"
        ])

        claims_ids = [c.claim_id for c in research.claims] if research.claims else []
        fact1 = research.facts[0] if research.facts else "This breakthrough workflow completely shifts the game."
        fact2 = research.facts[1] if len(research.facts) > 1 else "It delivers high aesthetic quality with 0 local GPU cost."
        fact3 = research.facts[2] if len(research.facts) > 2 else "Verified benchmarks confirm 90%+ viral hold rate."

        clean_topic = topic.replace(":", " -")

        if is_genz_aesthetic:
            # High-Retention Clumsy GenZ Hot Baddie & Aesthetic AI Character Storytelling
            hook = f"Tell me why being a clumsy aesthetic baddie in 2026 is an actual extreme sport! 😭✨"
            context = f"So I was trying to record my daily Pinterest morning aesthetic, and within five seconds I tripped over my Uggs and launched my iced matcha latte across the counter."
            core_value = f"Instead of crying, my AI character camera auto-rendered the spill into a 35mm Parisian editorial masterpiece. {fact1} No joke, {fact2}"
            proof = f"The secret? We are running serverless open-source video models with zero local GPU lag and pure 35mm film grain perfection. {fact3}"
            payoff = "You don't need a $4000 camera rig to look like a Pinterest board icon every single day."
            cta = "Drop a ✨ in the comments and subscribe for daily clumsy baddie lifestyle hacks and aesthetic AI secrets!"

            segments = [
                ScriptSegment(
                    id="scene_001",
                    voiceover=hook,
                    duration=4.0,
                    visual_intent="Sophia the stylish clumsy GenZ girl spilling her iced matcha latte in a sunlit loft, candid 35mm film aesthetic, photorealistic, 8k",
                    claims=[claims_ids[0]] if claims_ids else []
                ),
                ScriptSegment(
                    id="scene_002",
                    voiceover=context,
                    duration=6.0,
                    visual_intent="Sophia laughing at the matcha spill on modern marble counter, oversized pastel loungewear, soft golden hour glow",
                    claims=[]
                ),
                ScriptSegment(
                    id="scene_003",
                    voiceover=core_value,
                    duration=12.0,
                    visual_intent="Split screen aesthetic transformation: messy kitchen turning into high-fashion Parisian café terrace photoshoot",
                    claims=[claims_ids[1]] if len(claims_ids) > 1 else []
                ),
                ScriptSegment(
                    id="scene_004",
                    voiceover=proof,
                    duration=6.0,
                    visual_intent="Sophia walking down Tokyo street at dusk in chic trench coat with glowing aesthetic phone screen",
                    claims=[claims_ids[2]] if len(claims_ids) > 2 else []
                ),
                ScriptSegment(
                    id="scene_005",
                    voiceover=f"{payoff} {cta}",
                    duration=6.0,
                    visual_intent="Sophia winking playfully at camera in cozy record store holding coffee, warm aesthetic lighting, smooth camera zoom",
                    claims=[]
                )
            ]
        else:
            # High-Energy Tech / AI Breakthrough Script
            hook = f"Hugging Face and open source AI just changed everything with {clean_topic.split('-')[0].strip()}!"
            context = f"Most creators and developers are still paying heavy cloud bills, while open source foundation models like Wan 2.2 and HunyuanVideo are running completely free in serverless pipelines."
            core_value = f"{fact1} In real testing, {fact2} You can integrate this directly into your autonomous pipeline in under sixty seconds."
            proof = f"According to official verified benchmarks: {fact3}"
            payoff = "This gives you full autonomous production power without spending a single dollar on high-end local GPUs."
            cta = "Subscribe to Rishabh AI Studio for the complete open-source master code and daily automation blueprints!"

            segments = [
                ScriptSegment(
                    id="scene_001",
                    voiceover=hook,
                    duration=4.0,
                    visual_intent=f"High-energy 3D holographic title sequence showing {topic[:40]} bursting into neon cyan and magenta particle streams",
                    claims=[claims_ids[0]] if claims_ids else []
                ),
                ScriptSegment(
                    id="scene_002",
                    voiceover=context,
                    duration=6.0,
                    visual_intent="Futuristic cybernetic cloud server architecture with glowing data flow lines and zero GPU cost badge",
                    claims=[]
                ),
                ScriptSegment(
                    id="scene_003",
                    voiceover=core_value,
                    duration=12.0,
                    visual_intent="Split-screen dynamic code terminal executing Wan 2.2 / HunyuanVideo serverless video synthesis in real-time",
                    claims=[claims_ids[1]] if len(claims_ids) > 1 else []
                ),
                ScriptSegment(
                    id="scene_004",
                    voiceover=proof,
                    duration=6.0,
                    visual_intent="3D volumetric bar chart racing upwards showing verified benchmark speedup metrics",
                    claims=[claims_ids[2]] if len(claims_ids) > 2 else []
                ),
                ScriptSegment(
                    id="scene_005",
                    voiceover=f"{payoff} {cta}",
                    duration=6.0,
                    visual_intent="Sleek glowing YouTube subscribe button animation with Rishabh AI Studio branding and pulsing neon bell icon",
                    claims=[]
                )
            ]

        total_est = sum(s.duration for s in segments)

        fallback = {
            "title_candidate": topic,
            "hook": hook,
            "context": context,
            "core_value": core_value,
            "proof": proof,
            "payoff": payoff,
            "cta": cta,
            "format": format,
            "estimated_duration_seconds": total_est,
            "segments": [s.model_dump() for s in segments]
        }

        sys_prompt = "You are the Master YouTube Script Agent. Write engaging, retention-optimized vertical Shorts scripts."
        user_prompt = f"Topic: {topic}, Niche: {'Pinterest Aesthetic GenZ' if is_genz_aesthetic else 'Tech AI'}, Research Facts: {research.facts}, Format: {format}"

        res = await llm_service.generate_json(sys_prompt, user_prompt, fallback)
        plan = ScriptPlan(**res)

        audit_log("SCRIPT_GENERATED", {
            "topic": topic,
            "niche": "pinterest_genz" if is_genz_aesthetic else "tech_ai",
            "segments_count": len(plan.segments),
            "estimated_duration": plan.estimated_duration_seconds
        })

        return plan

script_agent = ScriptAgent()

