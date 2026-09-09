"""
Viral Boost & Retention Optimization Engine for Maya ✨ Cutie Baddie (/boost).
Optimizes video hook tension, seductive pattern interrupts, algorithm hashtags,
CTR thumbnail concepts, and YouTube SEO ranking factors for baddie psychology & dating secrets.
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

        # Power words that drive viral Shorts retention for Maya ✨
        power_words = [
            "spotted", "secret", "obsessed", "never", "everyone", "shocking", "trick",
            "insane", "clumsy", "baddie", "aesthetic", "pinterest", "babes", "tell me why",
            "pov", "relatable", "psychology", "mindblown", "nobody", "magnetic", "seductive",
            "alluring", "crush", "gossip", "tea", "unbothered", "glow", "glowup", "warned", "xoxo"
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

    def generate_boost_package(self, topic: str, hook: str, category: str = "Baddie Psychology & Magnetism") -> Dict[str, Any]:
        """
        Generates algorithm-optimized title candidates, hashtag matrix, and retention boost directives for Maya ✨.
        """
        logger.info(f"[BOOST] Generating algorithmic viral boost package for Maya ✨ topic: '{topic}'...")

        clean_topic = topic.replace(":", " -")
        core_topic = clean_topic.split('-')[0].strip()

        titles = [
            f"Spotted: {core_topic} ✨ (Gossip Girl Secret)",
            f"Spotted: The 3-Second Eye Contact Trick That Makes Him Obsessed ✨",
            f"Spotted: Why Being Unbothered Makes You 10x More Magnetic 💖"
        ]
        hashtags = [
            "#shorts",
            "#gossipgirl",
            "#mayabaddie",
            "#uppereastside",
            "#datingsecrets",
            "#psychologyhacks",
            "#darkfeminine",
            "#magnetic",
            "#aesthetic",
            "#glowup",
            "#relatable",
            "#crushhack",
            "#viral"
        ]
        pacing_directives = [
            "Scene 1 (0-4s): Seductive Gossip Girl pattern interrupt + instant curiosity hook ('Spotted: Maya spilling...').",
            "Scene 2 (4-9s): Upper East Side cafe terrace backstory + golden hour 35mm film still.",
            "Scene 3 (9-21s): Intimate Metropolitan Museum steps / penthouse boudoir revelation & psychological tea.",
            "Scene 4 (21-28s): 5th Avenue twilight glide & unbothered magnetic allure takeaway.",
            "Scene 5 (28-35s): Playful boudoir perfume spritz / wink payoff & 'XOXO, Maya ✨' comments CTA."
        ]

        hook_eval = self.evaluate_hook_strength(hook)

        boost_data = {
            "topic": topic,
            "niche": "pinterest_aesthetic_maya_cutie_baddie",
            "primary_title": titles[0],
            "ab_title_variants": titles,
            "hashtags": hashtags,
            "hook_evaluation": hook_eval,
            "retention_pacing": pacing_directives,
            "algorithm_boost_score": 98.8,
            "optimal_upload_hours": ["14:00 UTC", "18:30 UTC", "21:00 UTC"],
            "synthetic_media_declaration": True
        }

        audit_log("BOOST_PACKAGE_GENERATED", {
            "topic": topic,
            "boost_score": boost_data["algorithm_boost_score"]
        })

        return boost_data

boost_agent = BoostAgent()
