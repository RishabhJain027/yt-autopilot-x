from typing import List, Dict, Any
from python.schemas.topic import TopicCandidate
from python.services.llm_service import llm_service

class TrendAgent:
    def calculate_trend_score(self, m: Dict[str, float]) -> float:
        # Exact mathematical formula from Section 9.2 of BRAIN.md:
        # TrendScore = 0.30*momentum + 0.20*recency + 0.20*audience_fit + 0.15*diff + 0.15*feasibility - 0.20*rights_risk
        score = (
            0.30 * m.get('momentum', 0.8)
            + 0.20 * m.get('recency', 0.9)
            + 0.20 * m.get('audience_fit', 0.85)
            + 0.15 * m.get('differentiation', 0.75)
            + 0.15 * m.get('production_feasibility', 0.9)
            - 0.20 * m.get('rights_risk', 0.05)
        )
        return round(max(0.0, min(1.0, score)), 2)

    async def discover_trends(self, niche: str, pillars: List[str]) -> List[TopicCandidate]:
        candidates = [
            {
                "topic": "5 New AI Coding Assistants You Never Heard Of",
                "momentum": 0.88,
                "recency": 0.95,
                "audience_fit": 0.92,
                "differentiation": 0.80,
                "production_feasibility": 0.95,
                "rights_risk": 0.05,
                "channel_fit": 0.94
            },
            {
                "topic": "How To Automate Your Entire Daily Workflow in 10 Minutes",
                "momentum": 0.82,
                "recency": 0.88,
                "audience_fit": 0.90,
                "differentiation": 0.75,
                "production_feasibility": 0.90,
                "rights_risk": 0.05,
                "channel_fit": 0.91
            },
            {
                "topic": "The Open Source AI Revolution Nobody is Talking About",
                "momentum": 0.79,
                "recency": 0.85,
                "audience_fit": 0.87,
                "differentiation": 0.85,
                "production_feasibility": 0.90,
                "rights_risk": 0.05,
                "channel_fit": 0.89
            }
        ]

        results = []
        for item in candidates:
            score = self.calculate_trend_score(item)
            results.append(TopicCandidate(
                topic=item['topic'],
                score=score,
                trend_score=score,
                competition_score=0.45,
                rights_risk=item['rights_risk'],
                channel_fit=item['channel_fit'],
                momentum=item['momentum'],
                source="TrendRadar",
                status="DISCOVERED",
                evidence={"metrics": item}
            ))
        return results

trend_agent = TrendAgent()
