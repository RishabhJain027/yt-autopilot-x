from typing import Dict, Any, List
from python.schemas.channel import BrandKit
from python.services.llm_service import llm_service

class BrandingAgent:
    async def generate_brand_identity(self, niche: str) -> Dict[str, Any]:
        fallback = {
            "name": "Maya ✨ Cutie Baddie",
            "shortlist": ["Maya ✨ Cutie Baddie", "Maya Gossip Girl Diaries", "Spotted: Maya ✨", "The Manhattan Baddie Vault", "Maya Upper East Side"],
            "tagline": "Spotted: Seductive Psychology, Gossip Girl Tea & Manhattan Aesthetics",
            "channel_description": "Spotted: Maya spilling Manhattan's most scandalous secrets ✨ Daily tea on seductive psychology, high-society dating hacks, unbothered allure, and Gossip Girl baddie wisdom. Subscribe for your daily glow up babes. You know you love me... XOXO 💖",
            "logo_prompt": "Maya 21yo stunning Gossip Girl baddie, hazel eyes, glossy lips, blonde brunette blowout, luxury champagne silk dress, soft golden hour glow, Kodak Portra 400 35mm film still, photorealistic 8k, luxury minimalist circle logo",
            "banner_prompt": "Manhattan penthouse terrace overlooking New York skyline with iced matcha latte, silk robe, gold jewelry, warm golden hour, dreamy 35mm film still banner",
            "brand_kit": {
                "name": "Maya ✨ Cutie Baddie",
                "tone": ["gossip_girl", "seductive", "velvety", "alluring", "playful", "unbothered", "manhattan_luxury"],
                "primary_color": "#D4AF37",
                "secondary_color": "#180F1E",
                "logo_style": "aesthetic 35mm film portrait",
                "thumbnail_style": "Manhattan golden hour, Portra 400 film grain, Gossip Girl alluring baddie expression, clean frame"
            }
        }
        sys_prompt = "You are the Channel Branding Agent for Maya ✨ Cutie Baddie. Generate name ideas, shortlist, tagline, channel description, and visual identity for an intoxicating Gossip Girl baddie channel."
        user_prompt = f"Niche: {niche}. Generate brand kit without trademark conflicts."
        return await llm_service.generate_json(sys_prompt, user_prompt, fallback)

brand_agent = BrandingAgent()
