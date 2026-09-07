from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from database.schema import Channel, ChannelMemory
from python.schemas.channel import ChannelCreate
from python.schemas.api_response import ApiResponse
from python.schemas.topic import NicheScoreInput
from python.agents.niche_discovery import niche_agent
from python.agents.brand_agent import brand_agent
from packages.logger.logger import audit_log

router = APIRouter(prefix="/channels", tags=["Channels"])

@router.get("", response_model=ApiResponse[list])
async def list_channels(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Channel))
    channels = res.scalars().all()
    data = [{
        "id": c.id,
        "youtube_channel_id": c.youtube_channel_id,
        "title": c.title,
        "niche": c.niche,
        "operating_mode": c.operating_mode,
        "status": c.status,
        "created_at": c.created_at.isoformat() if c.created_at else None
    } for c in channels]
    return ApiResponse(data=data)

@router.post("", response_model=ApiResponse[dict])
async def create_channel(payload: ChannelCreate, db: AsyncSession = Depends(get_db)):
    ch = Channel(
        youtube_channel_id=payload.youtube_channel_id,
        title=payload.title or "Untitled Channel",
        description=payload.description,
        google_account_email=payload.google_account_email,
        niche=payload.niche,
        language_code=payload.language_code,
        timezone=payload.timezone,
        operating_mode=payload.operating_mode
    )
    db.add(ch)
    await db.commit()
    await db.refresh(ch)
    
    mem = ChannelMemory(channel_id=ch.id)
    db.add(mem)
    await db.commit()
    
    audit_log("CHANNEL_CREATED", {"channel_id": ch.id, "title": ch.title}, channel_id=ch.id)
    return ApiResponse(data={"id": ch.id, "title": ch.title, "youtube_channel_id": ch.youtube_channel_id})

@router.post("/{channel_id}/bootstrap", response_model=ApiResponse[dict])
async def bootstrap_channel(channel_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Channel).where(Channel.id == channel_id))
    ch = res.scalar_one_or_none()
    if not ch:
        raise HTTPException(status_code=404, detail="Channel not found")

    brand = await brand_agent.generate_brand_identity(ch.niche or "Technology Automation")
    
    mem_res = await db.execute(select(ChannelMemory).where(ChannelMemory.channel_id == channel_id))
    mem = mem_res.scalar_one_or_none()
    if mem:
        mem.brand_json = brand.get("brand_kit", {})
        mem.pillars_json = ["AI Tools", "Productivity Automation", "Tech Breakdowns"]
        await db.commit()

    return ApiResponse(data={"channel_id": channel_id, "brand": brand, "status": "BOOTSTRAP_COMPLETE"})

@router.post("/{channel_id}/niche/discover", response_model=ApiResponse[dict])
async def discover_niche_for_channel(channel_id: str, payload: NicheScoreInput, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Channel).where(Channel.id == channel_id))
    ch = res.scalar_one_or_none()
    if not ch:
        raise HTTPException(status_code=404, detail="Channel not found")

    proposal = await niche_agent.discover_niche(payload)
    ch.niche = proposal.niche
    await db.commit()
    return ApiResponse(data=proposal.model_dump())