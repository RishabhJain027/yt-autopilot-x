"""
Viral Boost & Retention Optimization Engine (/boost).
Optimizes video hook tension, pattern interrupts, algorithm hashtags,
CTR thumbnail concepts, and YouTube SEO ranking factors for Tech AI and Pinterest GenZ Lifestyle.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from python.schemas.script import ScriptPlan
from packages.logger.logger import logger, audit_log

class BoostAgent:
    def evaluate_hook_strength(self, hook_text: str) -> Dict[str, Any]:
        """
        Calculates Hook Impact Score (0-100) based on curiosity, urgency, and brevity.
        """
        words = hook_text.strip().split()
        word_count = len(words)

        # Power words that drive Shorts retention across Tech and GenZ Aesthetic niches
        power_words = [
            "new", "secret", "stop", "never", "everyone", "shocking", "breakthrough",
            "free", "faster", "insane", "hugging face", "open source", "ai", "leak",
            "clumsy", "baddie", "aesthetic", "pinterest", "besties", "tell me why", "pov", "relatable"
        ]
        matches = [w for w in words if w.lower().strip(".,!?:✨😭🚀") in power_words]

        # Scoring logic
        length_score = 100 if 5 <= word_count <= 18 else (70 if word_count < 5 else 60)
        power_score = min(100, max(60, len(matches) * 35))
        urgency_score = 95 if any(char in hook_text for char in ["!", "?", "😭", "✨", "🚀"]) else 75

        composite_score = round(0.40 * length_score + 0.40 * power_score + 0.20 * urgency_score, 1)

        return {
            "hook": hook_text,
            "impact_score": composite_score,
            "word_count": word_count,
            "power_keywords": matches,
            "verdict": "VIRAL_READY" if composite_score >= 80 else "ACCEPTABLE"
        }

    def generate_boost_package(self, topic: str, hook: str, category: str = "AI Tech") -> Dict[str, Any]:
        """
        Generates algorithm-optimized title candidates, hashtag matrix, and retention boost directives.
        """
        logger.info(f"[BOOST] Generating algorithmic viral boost package for '{topic}'...")

        topic_lower = topic.lower()
        is_genz_aesthetic = any(k in topic_lower or k in category.lower() for k in [
            "pinterest", "aesthetic", "genz", "baddie", "girl", "lifestyle", "character", "clumsy", "pov", "matcha"
        ])

        clean_topic = topic.replace(":", " -")

        if is_genz_aesthetic:
            titles = [
                f"{clean_topic} ✨ (Why Am I Like This?)",
                f"POV: You're That Clumsy Aesthetic Girl in 2026 😭",
                f"The Clumsy Baddie Guide to AI Lifestyle & Fashion 💖"
            ]
            hashtags = [
                "#shorts",
                "#aesthetic",
                "#pinterestvibes",
                "#clumsybaddie",
                "#genz",
                "#relatable",
                "#aicharacter",
                "#lifestyle",
                "#hotgirlwalk",
                "#ootd"
            ]
            pacing_directives = [
                "Scene 1 (0-3s): Maximum relatability hook + instant clumsy visual mishap.",
                "Scene 2 (3-8s): Laughable realization + aesthetic 35mm golden hour glow.",
                "Scene 3 (8-25s): High-fashion transformation / AI editorial makeover.",
                "Scene 4 (25-35s): Proof of seamless photorealistic aesthetic character vibe.",
                "Scene 5 (35-45s): Playful wink payoff & relatable comment CTA."
            ]
        else:
            titles = [
                f"{clean_topic} 🚀 (Nobody Saw This Coming)",
                f"Why {clean_topic.split('-')[0].strip()} Changes Everything in 2026",
                f"Stop Scrolling: {clean_topic} Is Finally Here!"
            ]
            hashtags = [
                "#shorts",
                "#ai",
                "#technology",
                "#huggingface",
                "#wan22",
                "#hunyuanvideo",
                "#opensource",
                "#aitools",
                "#futuretech",
                "#automation"
            ]
            pacing_directives = [
                "Scene 1 (0-3s): Maximum visual velocity with high-contrast motion graphic.",
                "Scene 2 (3-8s): Problem statement with zoomed-in interface highlight.",
                "Scene 3 (8-25s): Core technical demo with glowing step-by-step overlays.",
                "Scene 4 (25-35s): Proof benchmark comparison graph with audio pop.",
                "Scene 5 (35-45s): Direct subscriber payoff CTA with animated bell icon."
            ]

        hook_eval = self.evaluate_hook_strength(hook)

        boost_data = {
            "topic": topic,
            "niche": "pinterest_genz_lifestyle" if is_genz_aesthetic else "tech_ai_breakthroughs",
            "primary_title": titles[0],
            "ab_title_variants": titles,
            "hashtags": hashtags,
            "hook_evaluation": hook_eval,
            "retention_pacing": pacing_directives,
            "algorithm_boost_score": 95.8 if is_genz_aesthetic else 94.5,
            "optimal_upload_hours": ["14:00 UTC", "18:30 UTC", "21:00 UTC"],
            "synthetic_media_declaration": True
        }

        audit_log("BOOST_PACKAGE_GENERATED", {
            "topic": topic,
            "boost_score": boost_data["algorithm_boost_score"]
        })

        return boost_data

boost_agent = BoostAgent()

