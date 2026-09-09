"""
Master YouTube Script Agent.
Generates fast-paced, retention-optimized viral video scripts with 5-part structure:
Hook (0-2s) -> Context (2-8s) -> Core Value (8-25s) -> Proof/Benchmark (25-35s) -> Payoff & CTA (35-45s)
"""

from typing import Dict, Any, List
from python.schemas.script import ScriptPlan, ScriptSegment
from python.schemas.research import ResearchPacket
from python.services.llm_service import llm_service
from packages.logger.logger import logger, audit_log

class ScriptAgent:
    async def generate_script(self, topic: str, research: ResearchPacket, format: str = 'shorts') -> ScriptPlan:
        logger.info(f"[SCRIPT_AGENT] Generating high-retention {format} script for topic: '{topic}'...")

        # Extract facts & claims from research packet
        claims_ids = [c.claim_id for c in research.claims] if research.claims else []
        fact1 = research.facts[0] if research.facts else "This breakthrough model changes everything."
        fact2 = research.facts[1] if len(research.facts) > 1 else "It delivers state-of-the-art performance with 0 local GPU cost."
        fact3 = research.facts[2] if len(research.facts) > 2 else "Verified benchmarks confirm dramatic speed improvements."

        # Dynamically tailor hook and script segments to topic
        clean_topic = topic.replace(":", " -")
        
        hook = f"Hugging Face and open source AI just changed everything with {clean_topic.split('-')[0].strip()}!"
        context = f"Most creators and developers are still paying heavy cloud bills, while open source foundation models are running completely free in serverless pipelines."
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
                visual_intent="Split-screen dynamic code terminal executing Wan 2.1 Hugging Face serverless video synthesis in real-time",
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
        user_prompt = f"Topic: {topic}, Research Facts: {research.facts}, Format: {format}"

        res = await llm_service.generate_json(sys_prompt, user_prompt, fallback)
        plan = ScriptPlan(**res)
        
        audit_log("SCRIPT_GENERATED", {
            "topic": topic,
            "segments_count": len(plan.segments),
            "estimated_duration": plan.estimated_duration_seconds
        })

        return plan

script_agent = ScriptAgent()
