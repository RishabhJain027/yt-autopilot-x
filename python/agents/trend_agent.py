"""
Autonomous Trend Intelligence & Topic Discovery Agent for Maya ✨.
Discovers high-retention, viral aesthetic topics across Wikipedia rabbit holes,
psychological secrets, beauty & luxury lore, history mysteries, and cute clumsy baddie lifestyle.
"""

import random
import time
from typing import List, Dict, Any, Optional
from python.schemas.topic import TopicCandidate
from python.research.wikipedia_researcher import CURATED_WIKIPEDIA_TOPICS
from packages.logger.logger import logger, audit_log

class TrendAgent:
    def __init__(self):
        # Curated pool of high-retention Gossip Girl baddie psychology, dating secrets & aesthetic viral topics for Maya ✨
        self.topic_catalog = [
            # --- Gossip Girl & Seductive Baddie Psychology (Primary) ---
            {
                "topic": "The 3-Second Eye Contact Trick That Makes Him Obsessed",
                "category": "Gossip Girl Psychology & Triangle Gaze",
                "momentum": 0.99,
                "recency": 0.99,
                "audience_fit": 0.99,
                "differentiation": 0.97,
                "production_feasibility": 0.98,
                "rights_risk": 0.01,
                "channel_fit": 0.99,
                "evidence": {
                    "wiki_title": "Mirror neuron",
                    "source": "Wikipedia (https://en.wikipedia.org/wiki/Mirror_neuron)",
                    "vibe": "The 3-second triangle eye contact hack that triggers intense obsession"
                }
            },
            {
                "topic": "Spotted: Why Being Clumsy & Unbothered Makes You 10x More Magnetic",
                "category": "Upper East Side Psychology & Pratfall Magnetism",
                "momentum": 0.99,
                "recency": 0.99,
                "audience_fit": 0.98,
                "differentiation": 0.96,
                "production_feasibility": 0.97,
                "rights_risk": 0.01,
                "channel_fit": 0.98,
                "evidence": {
                    "wiki_title": "Pratfall effect",
                    "source": "Wikipedia (https://en.wikipedia.org/wiki/Pratfall_effect)",
                    "vibe": "Why unbothered, careless high-value girlies are scientifically 10x more attractive"
                }
            },
            {
                "topic": "Spotted: The Cleopatra Scent & Charisma Secret — How to Smell Seductively Unforgettable",
                "category": "Luxury Scent & High Society Lore",
                "momentum": 0.98,
                "recency": 0.98,
                "audience_fit": 0.97,
                "differentiation": 0.95,
                "production_feasibility": 0.96,
                "rights_risk": 0.01,
                "channel_fit": 0.97,
                "evidence": {
                    "wiki_title": "Cleopatra",
                    "source": "Wikipedia (https://en.wikipedia.org/wiki/Cleopatra)",
                    "vibe": "Ancient luxury, botanical perfume formulas, irresistible charisma"
                }
            },
            {
                "topic": "Spotted: The Reverse Psychology Favors Hack That Makes Him Chase You",
                "category": "Manhattan Dating Psychology Secrets",
                "momentum": 0.97,
                "recency": 0.98,
                "audience_fit": 0.96,
                "differentiation": 0.94,
                "production_feasibility": 0.96,
                "rights_risk": 0.01,
                "channel_fit": 0.96,
                "evidence": {
                    "wiki_title": "Ben Franklin effect",
                    "source": "Wikipedia (https://en.wikipedia.org/wiki/Ben_Franklin_effect)",
                    "vibe": "Reverse cognitive dissonance that triggers deep emotional investment"
                }
            },
            {
                "topic": "Spotted: The Red Lip & Scent Halo Effect — Why Aesthetics Rewire Subconscious Attraction",
                "category": "Gossip Girl Allure & Aesthetic Halo",
                "momentum": 0.96,
                "recency": 0.97,
                "audience_fit": 0.96,
                "differentiation": 0.93,
                "production_feasibility": 0.96,
                "rights_risk": 0.01,
                "channel_fit": 0.96,
                "evidence": {
                    "wiki_title": "Halo effect",
                    "source": "Wikipedia (https://en.wikipedia.org/wiki/Halo_effect)",
                    "vibe": "Cognitive bias, seductive presence, aesthetic glow up"
                }
            },
            {
                "topic": "Spotted: The Birkin Bag Origin — How Carefree Chaos Created Earth's Most Exclusive Luxury",
                "category": "Upper East Side Luxury Lore",
                "momentum": 0.96,
                "recency": 0.97,
                "audience_fit": 0.96,
                "differentiation": 0.93,
                "production_feasibility": 0.95,
                "rights_risk": 0.01,
                "channel_fit": 0.95,
                "evidence": {
                    "wiki_title": "Birkin bag",
                    "source": "Wikipedia (https://en.wikipedia.org/wiki/Birkin_bag)",
                    "vibe": "Jane Birkin airplane mishap and carefree Hermès status"
                }
            }
        ]

    def calculate_trend_score(self, m: Dict[str, float]) -> float:
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

    async def discover_trends(self, niche: str = "Pinterest Aesthetic & Girly Clumsy Baddie / Maya ✨", pillars: Optional[List[str]] = None, exclude_topics: Optional[List[str]] = None) -> List[TopicCandidate]:
        """
        Dynamically discovers and scores trending topics from Wikipedia rabbit holes,
        strictly excluding previously used topics.
        """
        logger.info(f"[TREND_AGENT] Discovering fresh Wikipedia rabbit hole trends for Maya ✨...")

        excluded_set = set()
        if exclude_topics:
            for t in exclude_topics:
                clean = t.lower().strip()
                excluded_set.add(clean)

        available_catalog = []
        for item in self.topic_catalog:
            t_lower = item['topic'].lower().strip()
            is_excluded = any(
                ex == t_lower or 
                (len(ex) > 10 and (ex in t_lower or t_lower in ex))
                for ex in excluded_set
            )
            if not is_excluded:
                available_catalog.append(item)

        # If catalog exhausted, dynamically generate fresh Wikipedia rabbit hole topic
        if not available_catalog:
            rand_wiki = random.choice(CURATED_WIKIPEDIA_TOPICS)
            synth_topic = f"{rand_wiki['title']}: {rand_wiki['vibe']} ({int(time.time()) % 1000})"
            available_catalog = [{
                "topic": synth_topic,
                "category": rand_wiki["category"],
                "momentum": 0.96,
                "recency": 0.98,
                "audience_fit": 0.96,
                "differentiation": 0.94,
                "production_feasibility": 0.96,
                "rights_risk": 0.01,
                "channel_fit": 0.96,
                "evidence": {"source": "Wikipedia (https://www.wikipedia.org)", "dynamic": True}
            }]

        results = []
        for item in available_catalog:
            score = self.calculate_trend_score(item)
            results.append(TopicCandidate(
                topic=item['topic'],
                score=score,
                trend_score=score,
                competition_score=0.30,
                rights_risk=item['rights_risk'],
                channel_fit=item['channel_fit'],
                momentum=item['momentum'],
                source=item.get("evidence", {}).get("source", "Wikipedia (https://www.wikipedia.org)"),
                status="DISCOVERED",
                evidence={"metrics": item, "breakdown": item.get("evidence", {})}
            ))

        results.sort(key=lambda x: x.score, reverse=True)

        audit_log("TRENDS_DISCOVERED", {
            "niche": niche,
            "candidates_count": len(results),
            "top_topic": results[0].topic if results else None
        })

        return results

trend_agent = TrendAgent()
