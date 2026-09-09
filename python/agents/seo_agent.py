"""
SEO & Publishing Metadata Agent for Maya ✨ Cutie Baddie.
Generates dreamy, alluring, high-CTR clickbait titles, juicy tea-spilling descriptions,
and viral hashtags that attract both girls and boys.
"""

from typing import List, Dict, Any
from python.schemas.production import PublishingPackage
from python.services.llm_service import llm_service

class SeoAgent:
    async def generate_metadata(self, topic: str, script_text: str) -> PublishingPackage:
        clean_topic = topic.replace(":", " -")
        core_topic = clean_topic.split('-')[0].strip()
        
        fallback = {
            "primary_title": f"Spotted: {core_topic} ✨ (Gossip Girl Secret)",
            "alternate_titles": [
                f"Spotted: The 3-Second Eye Contact Trick That Makes Him Obsessed ✨",
                f"Spotted: Why Being Unbothered Makes You 10x More Magnetic 😭💖",
                f"Spotted: The Upper East Side Psychology Secret Nobody Tells You ✨"
            ],
            "description": (
                f"Spotted: Maya spilling the juiciest tea on {clean_topic} ✨\n\n"
                "Welcome to Maya's daily Gossip Girl aesthetic diaries! "
                "Today we are diving into the most intoxicating psychological secrets and Upper East Side magnetic attraction hacks.\n\n"
                "💖 Drop a ✨ in the comments and subscribe to Maya for your daily Gossip Girl diaries, dating tea & high-society secrets!\n\n"
                "You know you love me... XOXO, Maya ✨\n\n"
                "#shorts #gossipgirl #mayabaddie #uppereastside #datingsecrets #psychologyhacks #darkfeminine #magnetic #aesthetic #glowup #relatable #crushhack #viral"
            ),
            "hashtags": [
                "#shorts", "#gossipgirl", "#mayabaddie", "#uppereastside",
                "#datingsecrets", "#psychologyhacks", "#darkfeminine", "#magnetic",
                "#aesthetic", "#glowup", "#relatable", "#crushhack", "#viral"
            ],
            "tags": [
                "gossip girl", "maya baddie", "upper east side", "seductive psychology",
                "dating hacks", "dark feminine", "magnetism secrets", "pratfall effect",
                "eye contact trick", "cleopatra scent", "glow up", "relatable tea", "shorts"
            ],
            "category_id": "22",  # People & Blogs / Entertainment
            "language": "en",
            "contains_synthetic_media": True
        }

        sys_prompt = (
            "You are the Viral SEO & Metadata Agent for Maya ✨ Cutie Baddie. "
            "Generate irresistible, dreamy, seductive clickbait titles, juicy tea-spilling aesthetic descriptions, "
            "and viral hashtags that attract both girls and boys. ZERO mentions of AI or tech jargon."
        )
        user_prompt = f"Topic: {topic}, Narration: {script_text[:200]}"
        res = await llm_service.generate_json(sys_prompt, user_prompt, fallback)
        return PublishingPackage(**res)

seo_agent = SeoAgent()
