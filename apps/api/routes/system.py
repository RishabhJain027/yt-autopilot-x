from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from database.schema import AuditLog
from packages.config.settings import settings
from packages.logger.logger import audit_log
from python.services.quota_manager import quota_manager
from python.services.budget_guard import budget_guard
from python.schemas.api_response import ApiResponse

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
            'video': settings.VIDEO_PROVIDER
        }
    })

@router.post('/emergency-stop', response_model=ApiResponse[dict])
async def toggle_emergency_stop(active: bool = True):
    settings.EMERGENCY_STOP = active
    audit_log('EMERGENCY_STOP_TOGGLED', {'active': active})
    return ApiResponse(data={'emergency_stop': settings.EMERGENCY_STOP})

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
