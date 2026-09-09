"""
Viral Boost & Retention Optimization Engine for Maya ✨ (/boost).
Optimizes video hook tension, aesthetic pattern interrupts, algorithm hashtags,
CTR thumbnail concepts, and YouTube SEO ranking factors for Wikipedia aesthetic rabbit holes.
"""

from typing import Dict, Any, List, Optional
from packages.logger.logger import logger, audit_log

class BoostAgent:
    def evaluate_hook_strength(self, hook_text: str) -> Dict[str, Any]:
        """
        Calculates Hook Impact Score (0-100) based on curiosity, urgency, and brevity.
        """
        words = hook_text.strip().split()
        word_count = len(words)

        # Power words that drive Shorts retention for Maya ✨
        power_words = [
            "new", "secret", "stop", "never", "everyone", "shocking", "breakthrough",
            "insane", "clumsy", "baddie", "aesthetic", "pinterest", "besties", "tell me why",
            "pov", "relatable", "wikipedia", "psychology", "mindblown", "nobody"
        ]
        matches = [w for w in words if w.lower().strip(".,!?:✨😭💖") in power_words]

        # Scoring logic
        length_score = 100 if 5 <= word_count <= 18 else (75 if word_count < 5 else 65)
        power_score = min(100, max(65, len(matches) * 35))
        urgency_score = 95 if any(char in hook_text for char in ["!", "?", "😭", "✨", "💖"]) else 75

        composite_score = round(0.40 * length_score + 0.40 * power_score + 0.20 * urgency_score, 1)

        return {
            "hook": hook_text,
            "impact_score": composite_score,
            "word_count": word_count,
            "power_keywords": matches,
            "verdict": "VIRAL_READY" if composite_score >= 80 else "ACCEPTABLE"
        }

    def generate_boost_package(self, topic: str, hook: str, category: str = "Aesthetic Psychology") -> Dict[str, Any]:
        """
        Generates algorithm-optimized title candidates, hashtag matrix, and retention boost directives for Maya ✨.
        """
        logger.info(f"[BOOST] Generating algorithmic viral boost package for Maya ✨ topic: '{topic}'...")

        clean_topic = topic.replace(":", " -")

        titles = [
            f"{clean_topic} ✨ (Why Nobody Talks About This)",
            f"POV: You Find This Psychological Secret on Wikipedia 😭✨",
            f"The Clumsy Baddie Guide to {clean_topic.split('-')[0].strip()} 💖"
        ]
        hashtags = [
            "#shorts",
            "#mayabaddie",
            "#aesthetic",
            "#psychologyfacts",
            "#wikipediarabbithole",
            "#pinterestvibes",
            "#clumsybaddie",
            "#genz",
            "#relatable",
            "#lifestyle",
            "#hotgirlwalk",
            "#ootd"
        ]
        pacing_directives = [
            "Scene 1 (0-3s): Seductive pattern interrupt + instant curiosity hook.",
            "Scene 2 (3-8s): Candid aesthetic backstory + soft 35mm golden hour glow.",
            "Scene 3 (8-22s): Shocking Wikipedia revelation & seductive breakdown.",
            "Scene 4 (22-30s): Scientific proof / psychological takeaway.",
            "Scene 5 (30-38s): Playful wink payoff & comment CTA for Maya ✨."
        ]

        hook_eval = self.evaluate_hook_strength(hook)

        boost_data = {
            "topic": topic,
            "niche": "pinterest_aesthetic_maya_baddie",
            "primary_title": titles[0],
            "ab_title_variants": titles,
            "hashtags": hashtags,
            "hook_evaluation": hook_eval,
            "retention_pacing": pacing_directives,
            "algorithm_boost_score": 98.2,
            "optimal_upload_hours": ["14:00 UTC", "18:30 UTC", "21:00 UTC"],
            "synthetic_media_declaration": True
        }

        audit_log("BOOST_PACKAGE_GENERATED", {
            "topic": topic,
            "boost_score": boost_data["algorithm_boost_score"]
        })

        return boost_data

boost_agent = BoostAgent()
