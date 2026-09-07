from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.connection import get_db
from database.schema import Channel, ChannelMemory
from python.services.youtube_service import youtube_service
from python.schemas.api_response import ApiResponse
from packages.logger.logger import audit_log

router = APIRouter(prefix="/oauth", tags=["OAuth"])

@router.get("/google/start")
async def oauth_start():
    url = youtube_service.generate_auth_url()
    return ApiResponse(data={"auth_url": url})

@router.get("/google/callback")
async def oauth_callback(code: str = Query(...), db: AsyncSession = Depends(get_db)):
    tokens = await youtube_service.exchange_code_for_tokens(code)
    
    ch_id = tokens.get("channel_id", "UC_CONNECTED")
    res = await db.execute(select(Channel).where(Channel.youtube_channel_id == ch_id))
    ch = res.scalar_one_or_none()
    if not ch:
        ch = Channel(
            youtube_channel_id=ch_id,
            title=tokens.get("channel_title", "My YouTube Channel"),
            google_account_email=tokens.get("email"),
            encrypted_refresh_token=tokens.get("refresh_token"),
            oauth_scopes=tokens.get("scopes")
        )
        db.add(ch)
        await db.commit()
        await db.refresh(ch)
        mem = ChannelMemory(channel_id=ch.id)
        db.add(mem)
        await db.commit()
    else:
        ch.encrypted_refresh_token = tokens.get("refresh_token")
        ch.oauth_scopes = tokens.get("scopes")
        await db.commit()

    awdit_log("OAUTH_CONNECTION_SUCCESS", {"channel_id": ch.id, "email": tokens.get("email")}, channel_id=ch.id)
    return ApiResponse(data={"status": "CONNECTED", "channel_id": ch.id, "title": ch.title})

@router.get("/mock-connect")
async def oauth_mock_connect(db: AsyncSession = Depends(get_db)):
    tokens = await youtube_service.exchange_code_for_tokens("mock_auth_code_123")
    res = await db.execute(select(Channel).where(Channel.youtube_channel_id == tokens["channel_id"]))
    ch = res.scalar_one_or_none()
    if not ch:
        ch = Channel(
            youtube_channel_id=tokens["channel_id"],
            title=tokens["channel_title"],
            google_account_email=tokens["email"],
            encrypted_refresh_token=tokens["refresh_token"],
            oauth_scopes=tokens["scopes"],
            niche="AI Tools & Productivity Automation"
        )
        db.add(ch)
        await db.commit()
        await db.refresh(ch)
        mem = ChannelMemory(channel_id=ch.id)
        db.add(mem)
        await db.commit()
    return ApiResponse(data={"status": "CONNECTED_SANDBOX", "channel_id": ch.id, "title": ch.title})
