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
            "primary_title": f"{core_topic} ✨ (The Seductive Baddie Secret)",
            "alternate_titles": [
                f"The 3-Second Trick That Makes Him Obsessed ✨",
                f"Why Being Unbothered Makes You 10x More Magnetic 😭💖",
                f"POV: You Find This Seductive Psychology Secret at 2AM ✨"
            ],
            "description": (
                f"Okay babes, come closer... let's spill the tea on {clean_topic} ✨\n\n"
                "Welcome to Maya's daily aesthetic tea & baddie diaries! "
                "Today we are diving into the most intoxicating psychological secrets and magnetic attraction hacks.\n\n"
                "💖 Drop a ✨ in the comments and subscribe to Maya for your daily baddie workflows, dating tea & seductive psychology secrets!\n\n"
                "#shorts #mayabaddie #baddievibes #pinterestgirl #datingsecrets #psychologyhacks #darkfeminine #magnetic #aesthetic #glowup #relatable #crushhack #viral"
            ),
            "hashtags": [
                "#shorts", "#mayabaddie", "#baddievibes", "#pinterestgirl",
                "#datingsecrets", "#psychologyhacks", "#darkfeminine", "#magnetic",
                "#aesthetic", "#glowup", "#relatable", "#crushhack", "#viral"
            ],
            "tags": [
                "maya baddie", "seductive girl", "pinterest aesthetic", "baddie psychology",
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
