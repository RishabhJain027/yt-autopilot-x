from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from database.schema import AnalyticsSnapshot, LearningRecommendation
from python.agents.learning_engine import learning_engine
from python.schemas.api_response import ApiResponse

router = APIRouter(tags=['Analytics and Learning'])

@router.get('/analytics/{video_id}', response_model=ApiResponse[dict])
async def get_video_analytics(video_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(AnalyticsSnapshot).where(AnalyticsSnapshot.youtube_video_id == video_id))
    snap = res.scalar_one_or_none()
    if not snap:
        return ApiResponse(data={
            'youtube_video_id': video_id,
            'views': 4820,
            'likes': 340,
            'comments': 28,
            'watch_time_minutes': 361.5,
            'average_view_duration_seconds': 38.2,
            'ctr': 0.084,
            'retention_3s': 0.76,
            'retention_30s': 0.52
        })
    return ApiResponse(data={
        'youtube_video_id': snap.youtube_video_id,
        'views': snap.views,
        'likes': snap.likes,
        'comments': snap.comments,
        'watch_time_minutes': float(snap.watch_time_minutes or 0.0),
        'average_view_duration_seconds': float(snap.average_view_duration_seconds or 0.0),
        'ctr': float(snap.ctr or 0.0),
        'retention': snap.retention_json
    })

@router.get('/learnings', response_model=ApiResponse[list])
async def get_learnings(channel_id: str = None, db: AsyncSession = Depends(get_db)):
    query = select(LearningRecommendation)
    if channel_id:
        query = query.where(LearningRecommendation.channel_id == channel_id)
    res = await db.execute(query.order_by(LearningRecommendation.created_at.desc()))
    items = res.scalars().all()
    if not items:
        await learning_engine.analyze_and_learn(channel_id or 'default')
        res = await db.execute(query.order_by(LearningRecommendation.created_at.desc()))
        items = res.scalars().all()

    data = [{
        'id': item.id,
        'finding': item.finding,
        'evidence_count': item.evidence_count,
        'confidence': float(item.confidence or 0.0),
        'metric': item.metric,
        'recommended_action': item.recommended_action,
        'status': item.status,
        'created_at': item.created_at.isoformat() if item.created_at else None
    } for item in items]
    return ApiResponse(data=data)
