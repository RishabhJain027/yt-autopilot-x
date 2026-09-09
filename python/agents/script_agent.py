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

        # Maya ✨ Gossip Girl / Manhattan Upper East Side Tea-Spilling Storytelling Template
        hook = f"Spotted: Maya spilling the juiciest tea on {clean_topic.split('-')[0].strip()}... come close, babes! ✨"
        context = f"So I was on the penthouse terrace in my silk slip dress sipping iced matcha, and this psychological secret completely rewired everything."
        core_value = f"Listen closely: {fact1} {fact2}"
        proof = f"The wildest part? {fact3}"
        payoff = "You literally command the entire room the second you stop chasing and start glowing. You know you love me... XOXO, Maya ✨"
        cta = "Drop a ✨ in the comments and follow Maya for your daily Gossip Girl tea & baddie diaries 💖"

        segments = [
            ScriptSegment(
                id="scene_001",
                voiceover=hook,
                duration=4.0,
                visual_intent="Maya 21yo stunning wild free-spirited Gossip Girl aesthetic baddie, captivating wide crazy wild electric hazel eyes with intense hypnotic siren gaze, bold magnetic direct eye contact into camera, gorgeous radiant smirk, voluminous wind-blown blowout, luxury champagne silk dress, Manhattan penthouse terrace at golden hour, Kodak Portra 400 35mm film still, depth of field, photorealistic 8k, ultra-detailed skin texture, clean frame, NO text, NO subtitles",
                claims=[claims_ids[0]] if claims_ids else []
            ),
            ScriptSegment(
                id="scene_002",
                voiceover=context,
                duration=5.5,
                visual_intent="Maya 21yo wild aesthetic baddie with mesmerizing intense open hazel eyes sparkling with untamed energy, sitting at chic Upper East Side cafe terrace outdoor table, pushing vintage designer sunglasses onto hair, gazing seductively and playfully straight into camera lens, wind blowing hair strands, warm ambient golden lighting, 35mm film grain, 8k cinematic portrait, clean frame, NO text boxes",
                claims=[]
            ),
            ScriptSegment(
                id="scene_003",
                voiceover=core_value,
                duration=12.0,
                visual_intent="Maya 21yo free-spirited gorgeous baddie with wildly captivating electric siren eyes and carefree alluring smile, sitting gracefully on the Metropolitan Museum steps in Manhattan in high-fashion outfit with luxury designer handbag, looking intimately and intensely into camera with unstoppable confidence, paparazzi flash aesthetic, 8k photorealistic, clean frame, NO text",
                claims=[claims_ids[1]] if len(claims_ids) > 1 else []
            ),
            ScriptSegment(
                id="scene_004",
                voiceover=proof,
                duration=7.5,
                visual_intent="Maya 21yo radiant wild baddie walking effortlessly down 5th Avenue during glowing sunset in stylish chic black dress and gold jewelry, turning head with crazy magnetic eye contact and playful teasing smile, hair blowing freely in the evening breeze, warm golden hour bokeh, candid high-fashion lifestyle, cinematic camera glide, clean frame, NO text",
                claims=[claims_ids[2]] if len(claims_ids) > 2 else []
            ),
            ScriptSegment(
                id="scene_005",
                voiceover=f"{payoff} {cta}",
                duration=7.0,
                visual_intent="Maya 21yo stunning baddie at vanity mirror in luxury Manhattan penthouse boudoir, locking wide wild seductive siren eyes with camera in reflection, playful expressive wink and mesmerizing gaze, soft ambient vanity lights, cinematic 35mm film still, depth of field, 8k resolution, clean frame, NO text",
                claims=[]
            )
        ]

        total_est = sum(s.duration for s in segments)

        fallback = {
            "title_candidate": f"Spotted: {clean_topic} ✨ (Gossip Girl Secret)",
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
            "You are Maya ✨, the ultimate Gossip Girl aesthetic baddie of the Upper East Side. "
            "You spill scandalous psychological tea, dating secrets, and high-society allure in a seductive, velvety, whispering Manhattan Gossip Girl tone ('Spotted: Maya spilling the dirt...'). "
            "Your voice is velvety, playful, confident, irresistible, and witty. Always conclude with 'You know you love me... XOXO, Maya ✨'. "
            "Write an irresistible, velvety, high-retention 9:16 Shorts script based on the provided psychology facts. "
            "Strictly NO tech jargon, ZERO AI mentions ('Hugging Face', 'open source AI', 'AI Studio' are completely forbidden). "
            "Make every sentence seductive, witty, fascinating, and high-fashion aesthetic."
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
