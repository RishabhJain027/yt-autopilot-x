from typing import List, Dict, Any
from python.schemas.production import PublishingPackage
from python.services.llm_service import llm_service

class SeoAgent:
    async def generate_metadata(self, topic: str, script_text: str) -> PublishingPackage:
        fallback = {
            "primary_title": f"{topic} (Step-by-Step)",
            "alternate_titles": [
                f"How {topic} Changes Everything",
                f"The Truth About {topic}",
                f"Why You Need {topic} Right Now"
            ],
            "description": (
                f"{topic}\n\n"
                "In this video, we break down the exact strategies and automated pipelines "
                "to streamline your workflow and master YouTube automation.\n\n"
                "?? Key Chapters:\n"
                "0:00 - Introduction & Hook\n"
                "0:10 - Core Value & Breakdown\n"
                "0:30 - Proof & Payoff\n"
                "0:45 - Next Steps\n\n"
                "?? Learn more in our documentation.\n"
                "?? Note: Synthetic media and AI assistance were utilized in the creation of this video."
            ),
            "hashtags": ["#AI", "#Automation", "#Tech", "#Productivity", "#Shorts"],
            "tags": ["ai automation", "productivity tools", "coding agents", "youtube autopilot", "tech tutorial"],
            "category_id": "28", # Science & Technology
            "language": "en",
            "contains_synthetic_media": True
        }

        sys_prompt = "You are the SEO & Metadata Agent. Generate high CTR truthful titles, descriptions, and tags."
        user_prompt = f"Topic: {topic}"
        res = await llm_service.generate_json(sys_prompt, user_prompt, fallback)
        return PublishingPackage(**res)

seo_agent = SeoAgent()
