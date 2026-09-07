from typing import Dict, Any, List
from python.schemas.channel import BrandKit
from python.services.llm_service import llm_service

class BrandingAgent:
    async def generate_brand_identity(self, niche: str) -> Dict[str, Any]:
        fallback = {
            "name": "FutureStack AI",
            "shortlist": ["FutureStack AI", "NeuroAutomate", "NextGen Stack", "Cognitive Workflow", "PromptCraft Tech"],
            "tagline": "Practical AI Tools & Automation That Actually Saves You Time",
            "channel_description": "We explore cutting-edge AI software, developer tools, and workflow automations to 10x your productivity. New breakdowns every day.",
            "logo_prompt": "Minimalist geometric hexagon with glowing cyan neural lines on deep slate background, vector logo, 8k",
            "banner_prompt": "Futuristic clean workspace with neon accent lighting and abstract digital grid, wide 16:9 banner",
            "brand_kit": {
                "name": "FutureStack AI",
                "tone": ["smart", "fast", "practical", "evidence-led"],
                "primary_color": "#0284C7",
                "secondary_color": "#0F172A",
                "logo_style": "minimal geometric",
                "thumbnail_style": "high contrast, one focal object, 3-5 words max"
            }
        }
        sys_prompt = "You are the Channel Branding Agent. Generate 50 name ideas, shortlist, tagline, channel description, and visual identity."
        user_prompt = f"Niche: {niche}. Generate brand kit without trademark conflicts."
        return await llm_service.generate_json(sys_prompt, user_prompt, fallback)

brand_agent = BrandingAgent()
