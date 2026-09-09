from typing import Dict, Any, List
from python.schemas.channel import BrandKit
from python.services.llm_service import llm_service

class BrandingAgent:
    async def generate_brand_identity(self, niche: str) -> Dict[str, Any]:
        fallback = {
            "name": "Maya ✨ Cutie Baddie",
            "shortlist": ["Maya ✨ Cutie Baddie", "Maya Baddie Diaries", "Aesthetic Maya ✨", "The Baddie Vault", "Maya Unbothered"],
            "tagline": "Seductive Psychology, Baddie Secrets & Pinterest Aesthetics",
            "channel_description": "Welcome to Maya's daily aesthetic diaries ✨ We spill intoxicating tea on seductive psychology, dating hacks, high-value allure, and magnetic baddie secrets. Subscribe for your daily glow up babes 💖",
            "logo_prompt": "Maya 21yo stunning gorgeous aesthetic baddie, hazel eyes, dreamy lips, messy bun, silk slip dress, soft golden hour glow, Kodak Portra 400 35mm film still, photorealistic 8k, luxury minimalist circle logo",
            "banner_prompt": "Aesthetic sunlit Parisian loft with iced matcha latte, silk robe, velvet cushions, floating golden dust, dreamy 35mm film still banner",
            "brand_kit": {
                "name": "Maya ✨ Cutie Baddie",
                "tone": ["seductive", "velvety", "alluring", "playful", "unbothered", "dreamy"],
                "primary_color": "#EC4899",
                "secondary_color": "#180F1E",
                "logo_style": "aesthetic 35mm film portrait",
                "thumbnail_style": "dreamy golden hour, Portra 400 film grain, alluring baddie expression, clean frame"
            }
        }
        sys_prompt = "You are the Channel Branding Agent for Maya ✨ Cutie Baddie. Generate name ideas, shortlist, tagline, channel description, and visual identity for an intoxicating Pinterest baddie channel."
        user_prompt = f"Niche: {niche}. Generate brand kit without trademark conflicts."
        return await llm_service.generate_json(sys_prompt, user_prompt, fallback)

brand_agent = BrandingAgent()
