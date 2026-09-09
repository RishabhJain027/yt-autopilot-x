"""
SEO & Publishing Metadata Agent for Maya ✨.
Generates aesthetic, high-CTR titles, descriptions, and tags for Shorts based on
fascinating Wikipedia research rabbit holes.
"""

from typing import List, Dict, Any
from python.schemas.production import PublishingPackage
from python.services.llm_service import llm_service

class SeoAgent:
    async def generate_metadata(self, topic: str, script_text: str) -> PublishingPackage:
        clean_topic = topic.replace(":", " -")
        fallback = {
            "primary_title": f"{clean_topic} ✨ (Wikipedia Rabbit Hole)",
            "alternate_titles": [
                f"Why {clean_topic.split('-')[0].strip()} is Mindblowing ✨",
                f"The Shocking Secret About {clean_topic.split('-')[0].strip()} 😭",
                f"POV: You Find This Secret on Wikipedia at 2AM ✨"
            ],
            "description": (
                f"{clean_topic} ✨\n\n"
                "Welcome to Maya's daily aesthetic rabbit holes & baddie diaries! "
                "Today we are diving into one of the most fascinating secrets documented on Wikipedia.\n\n"
                "✨ Source: Wikipedia, The Free Encyclopedia (https://www.wikipedia.org)\n"
                "💖 Drop a ✨ in the comments and subscribe to Maya for daily aesthetic psychology, history mysteries & lifestyle vibes!\n\n"
                "#shorts #mayabaddie #aesthetic #psychologyfacts #wikipediarabbithole #pinterestvibes #genz #relatable"
            ),
            "hashtags": ["#shorts", "#mayabaddie", "#aesthetic", "#psychologyfacts", "#wikipediarabbithole", "#pinterestvibes", "#genz", "#relatable"],
            "tags": ["maya baddie", "aesthetic psychology", "wikipedia rabbit hole", "pratfall effect", "cleopatra secrets", "girly facts", "pinterest aesthetic", "genz lifestyle", "shorts"],
            "category_id": "22",  # People & Blogs / Entertainment
            "language": "en",
            "contains_synthetic_media": True
        }

        sys_prompt = "You are the SEO & Metadata Agent for Maya ✨. Generate high CTR aesthetic titles, descriptions with Wikipedia citations, and viral tags."
        user_prompt = f"Topic: {topic}, Narration: {script_text[:200]}"
        res = await llm_service.generate_json(sys_prompt, user_prompt, fallback)
        return PublishingPackage(**res)

seo_agent = SeoAgent()
