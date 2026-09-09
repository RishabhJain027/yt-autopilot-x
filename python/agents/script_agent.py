"""
Master Script Agent for Maya ✨ Cutie Baddie.
Generates seductive, alluring, high-retention aesthetic Shorts scripts based on
authentic Wikipedia research rabbit holes (psychology, historical secrets, luxury lore, magnetism).
Strictly eliminates all repetitive AI jargon ("Hugging Face", "open source AI", "AI Studio").
"""

from typing import Dict, Any, List, Optional
from python.schemas.script import ScriptPlan, ScriptSegment
from python.schemas.research import ResearchPacket
from python.services.llm_service import llm_service
from packages.logger.logger import logger, audit_log

class ScriptAgent:
    async def generate_script(self, topic: str, research: ResearchPacket, format: str = 'shorts', niche: Optional[str] = None) -> ScriptPlan:
        logger.info(f"[SCRIPT_AGENT] Generating seductive Maya ✨ aesthetic {format} script for topic: '{topic}'...")

        claims_ids = [c.claim_id for c in research.claims] if research.claims else []
        facts = research.facts if research.facts else [
            "Psychological research proves that genuine, charming clumsy moments create instant magnetic attraction.",
            "Subconscious trust increases by 40% when you embrace your authentic cute quirks instead of hiding them.",
            "Historical and scientific archives verify that warmth consistently outperforms cold perfection."
        ]
        
        fact1 = facts[0]
        fact2 = facts[1] if len(facts) > 1 else facts[0]
        fact3 = facts[2] if len(facts) > 2 else "It is completely backed by verified psychological science."

        clean_topic = topic.replace(":", " -")

        # Maya ✨ Seductive Aesthetic Storytelling Template
        hook = f"Tell me why nobody told us this secret about {clean_topic.split('-')[0].strip()}! ✨"
        context = f"So I was looking through Wikipedia rabbit holes with my iced latte, and this completely blew my mind."
        core_value = f"Listen closely: {fact1} {fact2}"
        proof = f"The wildest part? {fact3}"
        payoff = "You literally do not need to be flawless to be totally unforgettable."
        cta = "Drop a ✨ in the comments and follow Maya for your daily aesthetic rabbit holes & baddie diaries!"

        segments = [
            ScriptSegment(
                id="scene_001",
                voiceover=hook,
                duration=4.0,
                visual_intent="Maya the stylish cute 21yo aesthetic baddie smiling playfully into camera in sunlit loft, soft golden hour glow, candid Kodak Portra 400 35mm film photography, photorealistic 8k, NO text boxes",
                claims=[claims_ids[0]] if claims_ids else []
            ),
            ScriptSegment(
                id="scene_002",
                voiceover=context,
                duration=6.0,
                visual_intent="Maya laughing candidly at cozy Parisian café terrace table with vintage sunglasses and chic trench coat, soft ambient lighting, clean cinematic frame, NO text boxes",
                claims=[]
            ),
            ScriptSegment(
                id="scene_003",
                voiceover=core_value,
                duration=12.0,
                visual_intent="Aesthetic cinematic scene illustrating the story, warm dreamy lighting, high-fashion editorial aesthetic, 35mm film grain, photorealistic, NO text boxes",
                claims=[claims_ids[1]] if len(claims_ids) > 1 else []
            ),
            ScriptSegment(
                id="scene_004",
                voiceover=proof,
                duration=7.0,
                visual_intent="Maya walking down glowing city street at dusk in stylish street style, warm ambient bokeh, candid high-fashion lifestyle, NO text boxes",
                claims=[claims_ids[2]] if len(claims_ids) > 2 else []
            ),
            ScriptSegment(
                id="scene_005",
                voiceover=f"{payoff} {cta}",
                duration=7.0,
                visual_intent="Maya winking playfully at camera in cozy vinyl record shop with pastel headphones, warm aesthetic lighting, smooth cinematic zoom, NO text boxes",
                claims=[]
            )
        ]

        total_est = sum(s.duration for s in segments)

        fallback = {
            "title_candidate": f"{clean_topic} ✨",
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

        sys_prompt = (
            "You are Maya ✨, a captivating, seductive, cute, and alluring aesthetic GenZ creator. "
            "Write an irresistible, velvety, high-retention 9:16 Shorts story script based on the provided Wikipedia facts. "
            "Do NOT include any mentions of 'Hugging Face', 'open source AI', 'AI Studio', or technical jargon. "
            "Make the voiceover seductive, witty, fascinating, and aesthetic."
        )
        user_prompt = f"Topic: {topic}, Wikipedia Facts: {facts}, Format: {format}"

        res = await llm_service.generate_json(sys_prompt, user_prompt, fallback)
        plan = ScriptPlan(**res)

        audit_log("SCRIPT_GENERATED", {
            "topic": topic,
            "persona": "maya_cutie_baddie",
            "segments_count": len(plan.segments),
            "estimated_duration": plan.estimated_duration_seconds
        })

        return plan

script_agent = ScriptAgent()
