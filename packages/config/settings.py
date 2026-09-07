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

    # Open-Source <5B Remote T2V Cloud Models
    T2V_PRIMARY_MODEL: str = 'Wan-AI/Wan2.1-T2V-1.3B'
    T2V_FALLBACK_MODEL: str = 'zai-org/CogVideoX-2b'
    T2V_FAST_MODEL: str = 'Lightricks/LTX-Video'
    T2V_LEGACY_MODEL: str = 'ali-vilab/text-to-video-ms-1.7b'
    T2V_EXECUTION_MODE: str = 'remote_serverless'  # Strictly 0 local compute / 0 GPU VRAM

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
