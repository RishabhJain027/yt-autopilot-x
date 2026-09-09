from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from database.schema import AuditLog, Channel
from packages.config.settings import settings
from packages.logger.logger import audit_log
from python.services.quota_manager import quota_manager
from python.services.budget_guard import budget_guard
from python.schemas.api_response import ApiResponse
from python.agents.goal_agent import goal_agent
from python.agents.browser_researcher import browser_researcher
from python.agents.learning_engine import learning_engine
from python.agents.boost_agent import boost_agent

router = APIRouter(prefix='/system', tags=['System and Health'])

@router.get('/health', response_model=ApiResponse[dict])
async def system_health():
    return ApiResponse(data={
        'status': 'HEALTHY',
        'emergency_stop': settings.EMERGENCY_STOP,
        'autonomous_publishing': settings.AUTONOMOUS_PUBLISHING,
        'operating_mode': settings.DEFAULT_OPERATING_MODE,
        'youtube_quota_remaining': quota_manager.get_remaining_quota(),
        'daily_budget_usd': settings.DAILY_BUDGET_USD,
        'providers': {
            'llm': settings.LLM_PRIMARY_PROVIDER,
            'tts': settings.TTS_PROVIDER,
            'image': settings.IMAGE_PROVIDER,
            'video': settings.VIDEO_PROVIDER,
            't2v_primary_model': settings.T2V_PRIMARY_MODEL,
            't2v_execution_mode': settings.T2V_EXECUTION_MODE
        }
    })

@router.post('/emergency-stop', response_model=ApiResponse[dict])
async def toggle_emergency_stop(active: bool = True):
    settings.EMERGENCY_STOP = active
    audit_log('EMERGENCY_STOP_TOGGLED', {'active': active})
    return ApiResponse(data={'emergency_stop': settings.EMERGENCY_STOP})

@router.get('/goal', response_model=ApiResponse[dict])
async def get_goals(channel_id: Optional[str] = None):
    status = await goal_agent.get_channel_goal_status(channel_id)
    return ApiResponse(data=status)

@router.get('/browser', response_model=ApiResponse[list])
async def browse_research(query: Optional[str] = None):
    results = await browser_researcher.browse_trending_research(query)
    return ApiResponse(data=results)

@router.post('/learn', response_model=ApiResponse[list])
async def trigger_learn(channel_id: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    if not channel_id:
        res = await db.execute(select(Channel).limit(1))
        ch = res.scalars().first()
        channel_id = ch.id if ch else "default"
    findings = await learning_engine.analyze_and_learn(channel_id)
    return ApiResponse(data=findings)

@router.post('/boost', response_model=ApiResponse[dict])
async def boost_optimization(topic: str = "Wan 2.1 Video AI", hook: str = "Hugging Face just released Wan 2.1!"):
    pkg = boost_agent.generate_boost_package(topic, hook)
    return ApiResponse(data=pkg)

@router.get('/logs', response_model=ApiResponse[list])
async def get_audit_logs(limit: int = 50, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit))
    logs = res.scalars().all()
    data = [{
        'id': l.id,
        'channel_id': l.channel_id,
        'event_type': l.event_type,
        'details': l.details_json,
        'created_at': l.created_at.isoformat() if l.created_at else None
    } for l in logs]
    return ApiResponse(data=data)
