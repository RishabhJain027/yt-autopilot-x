from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from database.schema import Channel, Topic, Production, ReviewRecord, YouTubeVideo
from python.schemas.production import ProductionCreate
from python.schemas.api_response import ApiResponse
from python.pipelines.orchestrator import pipeline_orchestrator
from python.pipelines.state_machine import state_machine
from python.services.youtube_service import youtube_service
from packages.logger.logger import audit_log

router = APIRouter(prefix='/productions', tags=['Productions'])

@router.get('', response_model=ApiResponse[list])
async def list_productions(channel_id: str = None, db: AsyncSession = Depends(get_db)):
    query = select(Production)
    if channel_id:
        query = query.where(Production.channel_id == channel_id)
    res = await db.execute(query.order_by(Production.created_at.desc()))
    prods = res.scalars().all()
    data = [{
        'id': p.id,
        'channel_id': p.channel_id,
        'topic_id': p.topic_id,
        'status': p.status,
        'format': p.format,
        'title': p.script_json.get('title_candidate') if p.script_json else 'Untitled Video',
        'final_video_path': p.final_video_path,
        'thumbnail_path': p.thumbnail_path,
        'render_duration_seconds': float(p.render_duration_seconds or 0.0),
        'review': p.review_json,
        'created_at': p.created_at.isoformat() if p.created_at else None
    } for p in prods]
    return ApiResponse(data=data)

@router.post('', response_model=ApiResponse[dict])
async def create_production(payload: ProductionCreate, bg: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    topic_id = payload.topic_id
    if payload.custom_topic and not topic_id:
        top = Topic(channel_id=payload.channel_id, topic=payload.custom_topic, score=0.95, status='SELECTED')
        db.add(top)
        await db.commit()
        await db.refresh(top)
        topic_id = top.id

    prod = Production(channel_id=payload.channel_id, topic_id=topic_id, status='IDEA', format=payload.format)
    db.add(prod)
    await db.commit()
    await db.refresh(prod)
    bg.add_task(pipeline_orchestrator.run_production_pipeline, prod.id)
    return ApiResponse(data={'production_id': prod.id, 'status': 'IDEA', 'pipeline': 'RUNNING'})

@router.get('/{production_id}', response_model=ApiResponse[dict])
async def get_production(production_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Production).where(Production.id == production_id))
    p = res.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail='Production not found')
    return ApiResponse(data={
        'id': p.id,
        'channel_id': p.channel_id,
        'topic_id': p.topic_id,
        'status': p.status,
        'format': p.format,
        'script': p.script_json,
        'visuals': p.visual_json,
        'publishing': p.publishing_json,
        'review': p.review_json,
        'final_video_path': p.final_video_path,
        'thumbnail_path': p.thumbnail_path,
        'video_hash_sha256': p.video_hash_sha256,
        'duration': float(p.render_duration_seconds or 0.0)
    })

@router.post('/{production_id}/approve', response_model=ApiResponse[dict])
async def approve_production(production_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Production).where(Production.id == production_id))
    p = res.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail='Production not found')
    p.status = state_machine.transition(p.status, 'APPROVED', p.id, p.channel_id)
    audit_log('PRODUCTION_APPROVED', {'production_id': p.id}, channel_id=p.channel_id)
    await db.commit()
    return ApiResponse(data={'id': p.id, 'status': p.status})

@router.post('/{production_id}/reject', response_model=ApiResponse[dict])
async def reject_production(production_id: str, reason: str = 'Operator rejection', db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Production).where(Production.id == production_id))
    p = res.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail='Production not found')
    p.status = state_machine.transition(p.status, 'QA_FAILED', p.id, p.channel_id)
    audit_log('PRODUCTION_REJECTED', {'production_id': p.id, 'reason': reason}, channel_id=p.channel_id)
    await db.commit()
    return ApiResponse(data={'id': p.id, 'status': p.status, 'reason': reason})

@router.post('/{production_id}/upload', response_model=ApiResponse[dict])
async def upload_production(production_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Production).where(Production.id == production_id))
    p = res.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail='Production not found')
    if p.status not in ['APPROVED', 'RENDERED']:
        raise HTTPException(status_code=400, detail=f'Cannot upload production in status {p.status}. Must be APPROVED.')

    title = p.publishing_json.get('primary_title') or 'Autonomous Video'
    desc = p.publishing_json.get('description') or ''
    tags = p.publishing_json.get('tags') or []
    contains_synth = p.publishing_json.get('contains_synthetic_media', True)

    upload_res = await youtube_service.upload_video(
        channel_id=p.channel_id,
        video_path=p.final_video_path or '',
        title=title,
        description=desc,
        tags=tags,
        contains_synthetic_media=contains_synth
    )

    yt_vid = YouTubeVideo(
        production_id=p.id,
        youtube_video_id=upload_res.get('youtube_video_id'),
        upload_status=upload_res.get('upload_status'),
        privacy_status=upload_res.get('privacy_status'),
        contains_synthetic_media=upload_res.get('contains_synthetic_media'),
        response_json=upload_res
    )
    db.add(yt_vid)
    p.status = state_machine.transition(p.status, 'SCHEDULED', p.id, p.channel_id)
    await db.commit()
    return ApiResponse(data=upload_res)
