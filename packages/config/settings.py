import os
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # Core System
    APP_ENV: str = 'development'
    SECRET_KEY: str = '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'
    DATABASE_URL: str = 'sqlite+aiosqlite:///storage/autopilot.db'
    STORAGE_ROOT: str = './storage'
    LOG_LEVEL: str = 'INFO'

    # Operating Modes: RESEARCH_ONLY, DRAFT_ONLY, APPROVAL_FIRST, AUTONOMOUS, EMERGENCY_STOP
    DEFAULT_OPERATING_MODE: str = 'APPROVAL_FIRST'
    AUTONOMOUS_PUBLISHING: bool = False
    EMERGENCY_STOP: bool = False

    # Google / YouTube OAuth
    GOOGLE_CLIENT_ID: str = ''
    GOOGLE_CLIENT_SECRET: str = ''
    GOOGLE_REDIRECT_URI: str = 'http://localhost:8000/api/v1/oauth/google/callback'
    YOUTUBE_API_KEY: Optional[str] = None

    # LLM Providers (mock, gemini, openai, anthropic, groq)
    LLM_PRIMARY_PROVIDER: str = 'mock'
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None

    # TTS Providers (local, edge_tts, gtts, openai, elevenlabs)
    TTS_PROVIDER: str = 'local'
    ELEVENLABS_API_KEY: Optional[str] = None

    # Media / Image Providers (mock, openai, stability, procedural)
    IMAGE_PROVIDER: str = 'mock'
    VIDEO_PROVIDER: str = 'remote_t2v_router'
    STABILITY_API_KEY: Optional[str] = None
    RUNWAY_API_KEY: Optional[str] = None
    HF_TOKEN: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None

    # Remote Open-Source T2V & Video Cloud Models (0 Local GPU / 100% Serverless)
    T2V_WAN22_MODEL: str = 'Wan-AI/Wan2.2-T2V-A14B'
    T2V_WAN22_DIFFUSERS_MODEL: str = 'Wan-AI/Wan2.2-T2V-A14B-Diffusers'
    T2V_WAN22_TI2V_MODEL: str = 'Wan-AI/Wan2.2-TI2V-5B'
    T2V_WAN22_TI2V_DIFFUSERS_MODEL: str = 'Wan-AI/Wan2.2-TI2V-5B-Diffusers'
    T2V_WAN22_LIGHTNING_MODEL: str = 'lightx2v/Wan2.2-Lightning'
    T2V_PRIMARY_MODEL: str = 'Wan-AI/Wan2.1-T2V-1.3B'
    T2V_WAN21_DIFFUSERS_MODEL: str = 'Wan-AI/Wan2.1-T2V-1.3B-Diffusers'
    T2V_WAN21_14B_MODEL: str = 'Wan-AI/Wan2.1-T2V-14B'
    T2V_HUNYUAN_MODEL: str = 'tencent/HunyuanVideo-1.5'
    T2V_HUNYUAN_BASE_MODEL: str = 'tencent/HunyuanVideo'
    T2V_FAST_HUNYUAN_MODEL: str = 'FastVideo/FastHunyuan'
    T2V_FAST_HUNYUAN_H3_MODEL: str = 'FastVideo/FastVideo-FastH3-4-step-Preview-v1-VSA-DataFree'
    T2V_LTX_25_MODEL: str = 'Lightricks/LTX-2.5-Diffusers'
    T2V_FAST_MODEL: str = 'Lightricks/LTX-Video'
    T2V_MINIMAX_MODEL: str = 'MiniMaxAI/MiniMax-H3'
    T2V_COSMOS_MODEL: str = 'nvidia/Cosmos-1.0-Diffusion-7B-Text2World'
    T2V_ANIMATEDIFF_MODEL: str = 'ByteDance/AnimateDiff-Lightning'
    T2V_ANIMATELCM_MODEL: str = 'wangfuyun/AnimateLCM'
    T2V_FALLBACK_MODEL: str = 'zai-org/CogVideoX-2b'
    T2V_COGVIDEOX_5B_MODEL: str = 'zai-org/CogVideoX-5b'
    T2V_OPENSORA_MODEL: str = 'hpcai-tech/Open-Sora-v2'
    T2V_MOCHI_MODEL: str = 'genmo/mochi-1-preview'
    T2V_STEPVIDEO_MODEL: str = 'stepfun-ai/stepvideo-t2v'
    T2V_PYRAMID_SD3_MODEL: str = 'rain1011/pyramid-flow-sd3'
    T2V_PYRAMID_MINIFLUX_MODEL: str = 'rain1011/pyramid-flow-miniflux'
    T2V_ALLEGRO_MODEL: str = 'rhymes-ai/Allegro'
    T2V_HOTSHOT_XL_MODEL: str = 'hotshotco/Hotshot-XL'
    T2V_LONGCAT_MODEL: str = 'meituan-longcat/LongCat-Video'
    T2V_KREA_REALTIME_MODEL: str = 'krea/krea-realtime-video'
    T2V_I2VGEN_XL_MODEL: str = 'ali-vilab/i2vgen-xl'
    T2V_MODELSCOPE_DAMO_MODEL: str = 'ali-vilab/modelscope-damo-text-to-video-synthesis'
    T2V_DAMO_MS_MODEL: str = 'damo-vilab/text-to-video-ms-1.7b'
    T2V_LEGACY_MODEL: str = 'ali-vilab/text-to-video-ms-1.7b'
    T2V_ZEROSCOPE_MODEL: str = 'cerspense/zeroscope_v2_576w'
    T2V_EXECUTION_MODE: str = 'remote_serverless'  # Strictly 0 local compute / 0 GPU VRAM

    # Niche & Persona Configuration
    DEFAULT_NICHE: str = 'Pinterest Aesthetic & Girly Clumsy Baddie / Maya ✨'
    SECONDARY_NICHE: str = 'Wikipedia Rabbit Holes & Psychological Secrets'
    DEFAULT_VOICE_GENDER: str = 'female'  # Female seductive alluring voice
    DEFAULT_FEMALE_VOICE: str = 'en-US-AvaNeural'
    DEFAULT_MALE_VOICE: str = 'en-US-AvaNeural'

    # Budgets & Limits
    DAILY_BUDGET_USD: float = 25.0
    MONTHLY_BUDGET_USD: float = 500.0
    MAX_RENDER_QUEUE: int = 5
    MAX_UPLOAD_QUEUE: int = 3

    # Scheduler
    SCHEDULER_ENABLED: bool = True
    SCHEDULER_TIMEZONE: str = 'Asia/Kolkata'
    HOURLY_TICK_CRON: str = '0 * * * *'

settings = Settings()

