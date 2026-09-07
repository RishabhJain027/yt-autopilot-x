from python.schemas.script import ScriptPlan, ScriptSegment
from python.schemas.research import ResearchPacket
from python.services.llm_service import llm_service

class ScriptAgent:
    async def generate_script(self, topic: str, research: ResearchPacket, format: str = 'shorts') -> ScriptPlan:
        # Exact structure per Section 12 of BRAIN.md:
        # Hook (0-2s) -> Context (2-8s) -> Value/Proof (8-35s) -> Payoff (35-50s) -> CTA (50-60s)
        fallback = {
            "title_candidate": topic,
            "hook": "Stop wasting 3 hours every day on repetitive tasks.",
            "context": "Most creators and developers still do manual workflows that modern tools solve in seconds.",
            "core_value": "Here are the top automation strategies: First, connect your pipeline to structured event triggers. Second, leverage asynchronous agents to handle background work while you sleep.",
            "proof": "These exact workflows cut operational overhead by 70% in real-world benchmarks.",
            "payoff": "You get a fully autonomous channel running on autopilot without lifting a finger.",
            "cta": "Subscribe for the complete automation blueprint and master code.",
            "format": format,
            "estimated_duration_seconds": 45.0,
            "segments": [
                {
                    "id": "scene_001",
                    "voiceover": "Stop wasting 3 hours every day on repetitive tasks.",
                    "duration": 4.0,
                    "visual_intent": "Futuristic fast-paced motion graphics showing clock speeding up",
                    "claims": [research.claims[0].claim_id] if research.claims else []
                },
                {
                    "id": "scene_002",
                    "voiceover": "Most creators and developers still do manual workflows that modern tools solve in seconds.",
                    "duration": 6.0,
                    "visual_intent": "Screen showing complex tasks transforming into clean automated code",
                    "claims": []
                },
                {
                    "id": "scene_003",
                    "voiceover": "Here are the top automation strategies: First, connect your pipeline to structured event triggers. Second, leverage asynchronous agents to handle background work.",
                    "duration": 18.0,
                    "visual_intent": "Visual pipeline diagram showing multi-agent orchestration",
                    "claims": [research.claims[1].claim_id] if len(research.claims) > 1 else []
                },
                {
                    "id": "scene_004",
                    "voiceover": "These exact workflows cut operational overhead by 70% in real-world benchmarks.",
                    "duration": 8.0,
                    "visual_intent": "Data visualization dashboard with rising efficiency metrics",
                    "claims": []
                },
                {
                    "id": "scene_005",
                    "voiceover": "Subscribe for the complete automation blueprint and master code.",
                    "duration": 6.0,
                    "visual_intent": "Channel logo and animated subscribe call-to-action button",
                    "claims": []
                }
            ]
        }

        sys_prompt = "You are the Master YouTube Script Agent. Write engaging, fast-paced retention-optimized scripts."
        user_prompt = f"Topic: {topic}, Format: {format}"
        res = await llm_service.generate_json(sys_prompt, user_prompt, fallback)
        return ScriptPlan(**res)

script_agent = ScriptAgent()
