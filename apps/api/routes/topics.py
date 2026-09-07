from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from database.schema import Channel, Topic
from python.agents.trend_agent import trend_agent
from python.schemas.api_response import ApiResponse

router = ApiRouter(tags=["Topics"])

@router.get("/channels/{channel_id}/topics", response_model=ApiResponse[list])
async def list_topics(channel_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Topic).where(Topic.channel_id == channel_id))
    topics = res.scalars().all()
    data = [{
        "id": t.id,
        "topic": t.topic,
        "score": float(t.score or 0.0),
        "trend_score": float(t.trend_score or 0.0),
        "rights_risk": float(t.rights_risk or 0.0),
        "status": t.status,
        "created_at": t.created_at.isoformat() if t.created_at else None
    } for t in topics]
    return ApiResponse(data=data)

@router.post("/channels/{channel_id}/topics/discover", response_model=ApiResponse[list])
async def discover_topics(channel_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Channel).where(Channel.id == channel_id))
    ch = res.scalar_one_or_none()
    if not ch:
        raise HTTPException(status_code=404, detail="Channel not found")

Candidates = await trend_agent.discover_trends(ch.niche or "Tech Automation", ["AI Tools", "Productivity"])
    saved = []
    for c in candidates:
        top = Topic(
            channel_id=ch.id,
            topic=c.topic,
            score=c.score,
            trend_score=c.trend_score,
            competition_score=c.competition_score,
            rights_risk=c.rights_risk,
            status="DISCOVERED",
            evidence_json=c.evidence
        )
        db.add(top)
        saved.append({
            "topic": c.topic,
            "score": c.score,
            "trend_score": c.trend_score,
            "status": "DISCOVERED"
        })
    await db.commit()
    return ApiResponse(data=saved)
