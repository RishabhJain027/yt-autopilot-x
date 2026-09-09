"""
Master Script Agent for Maya ✨ Cutie Baddie.
Generates seductive, alluring, high-retention aesthetic Shorts scripts based on
fascinating baddie psychology, dating secrets, luxury lore, and magnetic charisma.
Strictly eliminates all repetitive AI jargon ("Hugging Face", "open source AI", "AI Studio").
"""

from typing import Dict, Any, List, Optional
from python.schemas.script import ScriptPlan, ScriptSegment
from python.schemas.research import ResearchPacket
from python.services.llm_service import llm_service
from packages.logger.logger import logger, audit_log

class ScriptAgent:
    async def generate_script(self, topic: str, research: ResearchPacket, format: str = 'shorts', niche: Optional[str] = None) -> ScriptPlan:
        logger.info(f"[SCRIPT_AGENT] Generating intoxicating, seductive Maya ✨ aesthetic {format} script for topic: '{topic}'...")

        claims_ids = [c.claim_id for c in research.claims] if research.claims else []
        facts = research.facts if research.facts else [
            "Psychological science proves that holding soft, alluring eye contact triggers instant dopamine synchronization in the brain.",
            "Subconscious attraction increases exponentially when you embrace unbothered high-value calm rather than chasing validation.",
            "Historical and behavioral research confirms that warm seductive charisma consistently creates uncontrollable magnetic obsession."
        ]
        
        fact1 = facts[0]
        fact2 = facts[1] if len(facts) > 1 else facts[0]
        fact3 = facts[2] if len(facts) > 2 else "It is completely proven by real behavioral psychology."

        clean_topic = topic.replace(":", " -")

        # Maya ✨ Seductive Baddie Tea-Spilling & Aesthetic Storytelling Template
        hook = f"Okay babes, come closer... tell me why nobody warned us about this secret of {clean_topic.split('-')[0].strip()}! ✨"
        context = f"So I was sipping my iced matcha in my silk robe, going down the juiciest psychology rabbit hole, and the tea is crazy."
        core_value = f"Listen closely: {fact1} {fact2}"
        proof = f"The wildest part? {fact3}"
        payoff = "You literally become completely irresistible the second you stop chasing and start glowing."
        cta = "Drop a ✨ in the comments and follow Maya for your daily aesthetic tea & baddie diaries 💖"

        segments = [
            ScriptSegment(
                id="scene_001",
                voiceover=hook,
                duration=4.0,
                visual_intent="Maya 21yo stunning gorgeous aesthetic baddie, captivating hazel eyes, dreamy lips, messy brunette bun with face-framing strands, oversized cream knit sweater, sunlit golden hour loft, soft natural glow, Kodak Portra 400 35mm film still, depth of field, photorealistic 8k, ultra-detailed skin texture, clean frame, NO text, NO subtitles",
                claims=[claims_ids[0]] if claims_ids else []
            ),
            ScriptSegment(
                id="scene_002",
                voiceover=context,
                duration=5.5,
                visual_intent="Maya sitting at chic Parisian cafe terrace outdoor table, chic vintage sunglasses pushed on head, oversized beige trench coat, sipping iced matcha latte, glancing seductively into camera with playful smile, warm ambient lighting, 35mm film grain, 8k cinematic portrait, clean frame, NO text boxes",
                claims=[]
            ),
            ScriptSegment(
                id="scene_003",
                voiceover=core_value,
                duration=12.0,
                visual_intent="Maya in a dreamy aesthetic boudoir room with soft velvet cushions and floating fairy lights, looking intimately into camera with alluring warm gaze, high-fashion editorial aesthetic, 8k photorealistic, clean frame, NO text",
                claims=[claims_ids[1]] if len(claims_ids) > 1 else []
            ),
            ScriptSegment(
                id="scene_004",
                voiceover=proof,
                duration=7.5,
                visual_intent="Maya walking gracefully down glowing city avenue during sunset in stylish chic streetwear, warm golden hour bokeh, candid high-fashion lifestyle, cinematic camera glide, clean frame, NO text",
                claims=[claims_ids[2]] if len(claims_ids) > 2 else []
            ),
            ScriptSegment(
                id="scene_005",
                voiceover=f"{payoff} {cta}",
                duration=7.0,
                visual_intent="Maya applying luxury botanical perfume with alluring playful expression, playful expressive wink at camera in sunlit bedroom, cinematic 35mm film still, depth of field, 8k resolution, clean frame, NO text",
                claims=[]
            )
        ]

        total_est = sum(s.duration for s in segments)

        fallback = {
            "title_candidate": f"{clean_topic} ✨ (Baddie Secret)",
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
            "You are Maya ✨, the ultimate seductive, alluring, captivating aesthetic baddie. "
            "You spill juicy psychological tea, dating secrets, and baddie wisdom in a dreamy, whispering, intoxicating Pinterest-girl aesthetic. "
            "Your voice is velvety, playful, confident, and irresistible to both girls and boys. "
            "Write an irresistible, velvety, high-retention 9:16 Shorts script based on the provided psychology facts. "
            "Strictly NO tech jargon, ZERO AI mentions ('Hugging Face', 'open source AI', 'AI Studio' are completely forbidden). "
            "Make every sentence seductive, witty, fascinating, and aesthetic."
        )
        user_prompt = f"Topic: {topic}, Facts: {facts}, Format: {format}"

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
