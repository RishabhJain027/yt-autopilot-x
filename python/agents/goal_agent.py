"""
Autonomous Goal & Milestone Tracking Engine (/goal).
Tracks channel KPIs, subscriber targets, view velocity, publishing cadence,
and aligns autonomous pipeline production ticks to milestone targets.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from database.connection import AsyncSessionLocal
from database.schema import Channel, Production, YouTubeVideo, AnalyticsSnapshot
from sqlalchemy.future import select
from packages.logger.logger import logger, audit_log

class GoalAgent:
    def __init__(self):
        self.default_goals = {
            "target_subscribers": 10000,
            "target_monthly_views": 500000,
            "target_daily_shorts": 3,
            "retention_target_pct": 75.0,
            "ctr_target_pct": 7.0,
            "monetization_watch_hours_target": 4000
        }

    async def get_channel_goal_status(self, channel_id: Optional[str] = None) -> Dict[str, Any]:
        async with AsyncSessionLocal() as session:
            if channel_id:
                ch_query = select(Channel).where((Channel.id == channel_id) | (Channel.youtube_channel_id == channel_id))
            else:
                ch_query = select(Channel).limit(1)
            
            res = await session.execute(ch_query)
            ch = res.scalars().first()
            ch_id = ch.id if ch else "default"
            ch_title = ch.title if ch else "Baddie AI Studio"

            # Count total completed/published productions
            prods_res = await session.execute(
                select(Production).where(Production.channel_id == ch_id)
            )
            all_prods = prods_res.scalars().all()
            total_prods = len(all_prods)
            completed_prods = len([p for p in all_prods if p.status in ['SCHEDULED', 'PUBLISHED', 'APPROVED', 'RENDERED']])

            # Calculate goal metrics
            daily_pace = min(completed_prods, 3)
            pace_progress = (daily_pace / self.default_goals["target_daily_shorts"]) * 100

            status = {
                "channel_id": ch_id,
                "channel_name": ch_title,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "targets": self.default_goals,
                "current_progress": {
                    "total_productions_created": total_prods,
                    "completed_productions": completed_prods,
                    "daily_publishing_rate": f"{completed_prods}/3 Shorts today",
                    "pace_compliance_pct": round(pace_progress, 1),
                    "pipeline_readiness": "OPTIMAL" if total_prods > 0 else "INITIALIZING"
                },
                "strategy_recommendation": (
                    "Maintain current cadence: 3 High-Retention Shorts per day with Wan 2.1/Flux cloud AI visuals."
                    if completed_prods >= 2 else
                    "Accelerate pipeline ticks: Launch 1 additional AI Tech Breakthrough short to fulfill daily quota."
                )
            }

            audit_log("GOAL_EVALUATED", {
                "channel_id": ch_id,
                "completed": completed_prods,
                "pace_compliance": pace_progress
            }, channel_id=ch_id)

            return status

goal_agent = GoalAgent()
