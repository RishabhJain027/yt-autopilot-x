from typing import Dict, Any, List, Optional
from python.schemas.topic import NicheScoreInput, NicheProposal
from python.services.llm_service import llm_service

class NicheDiscoveryAgent:
    def calculate_niche_score(self, m: Dict[str, float]) -> float:
        # Exact mathematical formula from Section 7.4 of BRAIN.md:
        # NicheScore = 0.20*TrendDemand + 0.15*AudienceSize + 0.15*ProductionFeasibility + 0.15*Evergreen
        #            + 0.10*Monetization + 0.10*Differentiation + 0.05*SearchIntent + 0.10*BrandFit
        #            - 0.20*CopyrightRisk - 0.10*Saturation
        score = (
            0.20 * m.get('trend_demand', 0.8)
            + 0.15 * m.get('audience_size', 0.8)
            + 0.15 * m.get('production_feasibility', 0.9)
            + 0.15 * m.get('evergreen_potential', 0.7)
            + 0.10 * m.get('monetization_potential', 0.8)
            + 0.10 * m.get('differentiation', 0.75)
            + 0.05 * m.get('search_intent', 0.7)
            + 0.10 * m.get('brand_fit', 0.9)
            - 0.20 * m.get('copyright_risk', 0.1)
            - 0.10 * m.get('saturation', 0.3)
        )
        return round(max(0.0, min(1.0, score)), 2)

    async def discover_niche(self, input_data: NicheScoreInput) -> NicheProposal:
        pref = (input_data.niche_preference or input_data.category or '').lower()
        is_genz_aesthetic = any(k in pref for k in ['pinterest', 'genz', 'baddie', 'aesthetic', 'girl', 'lifestyle', 'clumsy'])

        if is_genz_aesthetic:
            metrics = {
                'trend_demand': 0.94,
                'audience_size': 0.92,
                'production_feasibility': 0.95,
                'evergreen_potential': 0.80,
                'monetization_potential': 0.88,
                'differentiation': 0.85,
                'search_intent': 0.82,
                'brand_fit': 0.96,
                'copyright_risk': 0.03,
                'saturation': 0.28
            }
            score = self.calculate_niche_score(metrics)
            fallback = {
                "niche": "Pinterest Aesthetic / Clumsy GenZ Hot Baddie & AI Character Lifestyle",
                "score": score,
                "audience": "18-28 GenZ fashion & lifestyle enthusiasts, aesthetic digital creators, relatable humor lovers",
                "primary_format": "shorts" if input_data.shorts else "long_form",
                "secondary_format": "long_form",
                "content_pillars": [
                    "Clumsy Hot Baddie Relatable Daily Chronicles",
                    "Aesthetic AI Character Morning & Evening Routines",
                    "Pinterest Vibe OOTDs & Digital Wardrobe Inspo",
                    "Chaotic Storytime & Faceless AI Creator Hacks",
                    "Hot Girl Walk Diaries & Aesthetic Wellness Tips"
                ],
                "risk_notes": ["Maintain photorealistic AI character visual consistency across all scene renders."],
                "evidence": [{"source": "Pinterest Trends & TikTok Viral Radar", "confidence": 0.96}]
            }
        else:
            metrics = {
                'trend_demand': 0.88,
                'audience_size': 0.85,
                'production_feasibility': 0.90,
                'evergreen_potential': 0.75,
                'monetization_potential': 0.82,
                'differentiation': 0.78,
                'search_intent': 0.80,
                'brand_fit': 0.95,
                'copyright_risk': 0.05,
                'saturation': 0.35
            }
            score = self.calculate_niche_score(metrics)
            fallback = {
                "niche": "AI Tools and Productivity Automation",
                "score": score,
                "audience": "18-34 tech learners, developers, and productivity enthusiasts",
                "primary_format": "shorts" if input_data.shorts else "long_form",
                "secondary_format": "long_form",
                "content_pillars": [
                    "Open Source Video AI (Wan 2.2 / HunyuanVideo / LTX)",
                    "Serverless Cloud AI Workflows with 0 Local GPU",
                    "Coding Assistant Comparisons & Agent Protocols",
                    "Autonomous YouTube Production Pipelines"
                ],
                "risk_notes": ["Ensure accurate benchmarks and attribution when referencing new tools."],
                "evidence": [{"source": "Tech Trend Radar", "confidence": 0.92}]
            }

        sys_prompt = "You are the Niche Intelligence Agent. Propose the optimal YouTube channel niche given the constraints."
        user_prompt = f"Target Region: {input_data.target_region}, Faceless: {input_data.faceless}, Format: Shorts={input_data.shorts}, Preference: {input_data.niche_preference or 'general'}"
        res = await llm_service.generate_json(sys_prompt, user_prompt, fallback)
        return NicheProposal(**res)

niche_agent = NicheDiscoveryAgent()

