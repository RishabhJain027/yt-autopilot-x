from datetime import datetime, timezone
from sqlalchemy.future import select
from database.connection import AsyncSessionLocal
from database.schema import Channel, Topic, Production
from python.agents.trend_agent import trend_agent
from python.pipelines.orchestrator import pipeline_orchestrator
from python.services.quota_manager import quota_manager
from python.services.budget_guard import budget_guard
from packages.config.settings import settings
from packages.logger.logger import logger, audit_log

class HourlyTickOrchestrator:
    async def run_tick(self):
        logger.info("[HOURLY_TICK] === Starting autonomous hourly cycle ===")

        if settings.EMERGENCY_STOP:
            logger.warning("[HOURLY_TICK] Emergency stop is ACTIVE. Skipping production cycle.")
            return

        async with AsyncSessionLocal() as session:
            # 1. Fetch active channels
            res = await session.execute(select(Channel).where(Channel.status == 'ACTIVE'))
            channels = res.scalars().all()
            if not channels:
                logger.info("[HOURLY_TICK] No active channels configured. Creating demo channel profile.")
                demo = Channel(
                    youtube_channel_id="UC_DEMO_CHANNEL_001",
                    title="FutureStack AI Tech",
                    niche="AI Tools and Productivity",
                    operating_mode=settings.DEFAULT_OPERATING_MODE,
                    status="ACTIVE"
                )
                session.add(demo)
                await session.commit()
                channels = [demo]

            for ch in channels:
                logger.info(f"[HOURLY_TICK] Processing channel: {ch.title} ({ch.youtube_channel_id})")

                # Check Backlog
                pending_prods = await session.execute(
                    select(Production).where(
                        Production.channel_id == ch.id,
                        Production.status.in_(['IDEA', 'RESEARCHING', 'SCRIPTING', 'RENDERING', 'QA_PENDING'])
                    )
                )
                active_jobs = pending_prods.scalars().all()

                if len(active_jobs) >= settings.MAX_RENDER_QUEUE:
                    logger.info(f"[HOURLY_TICK] Backpressure limit reached ({len(active_jobs)} active jobs). Deferring new topic discovery.")
                    continue

                # Discover new trends & topics if backlog is low
                topics_res = await session.execute(
                    select(Topic).where(Topic.channel_id == ch.id, Topic.status == 'DISCOVERED')
                )
                available_topics = topics_res.scalars().all()

                if not available_topics:
                    logger.info(f"[HOURLY_TICK] Discovering new trends for {ch.niche or 'Tech'}...")
                    candidates = await trend_agent.discover_trends(ch.niche or "Tech Automation", ["AI Tools", "Productivity"])
                    for cand in candidates:
                        new_topic = Topic(
                            channel_id=ch.id,
                            topic=cand.topic,
                            score=cand.score,
                            trend_score=cand.trend_score,
                            competition_score=cand.competition_score,
                            rights_risk=cand.rights_risk,
                            status='DISCOVERED',
                            evidence_json=cand.evidence
                        )
                        session.add(new_topic)
                    await session.commit()
                    
                    # Refresh available topics
                    topics_res = await session.execute(
                        select(Topic).where(Topic.channel_id == ch.id, Topic.status == 'DISCOVERED')
                    )
                    available_topics = topics_res.scalars().all()

                # Pick highest scoring topic and launch production
                if available_topics:
                    top_topic = sorted(available_topics, key=lambda t: t.score or 0.0, reverse=True)[0]
                    top_topic.status = 'IN_PROGRESS'
                    
                    prod = Production(
                        channel_id=ch.id,
                        topic_id=top_topic.id,
                        status='IDEA',
                        format='shorts'
                    )
                    session.add(prod)
                    await session.commit()

                    logger.info(f"[HOURLY_TICK] Launched production {prod.id} for topic: {top_topic.topic}")
                    # Run production pipeline
                    try:
                        await pipeline_orchestrator.run_production_pipeline(prod.id)
                        top_topic.status = 'COMPLETED'
                        await session.commit()
                    except Exception as e:
                        logger.error(f"[HOURLY_TICK] Pipeline failed for production {prod.id}: {e}")

        logger.info("[HOURLY_TICK] === Hourly cycle complete ===")

hourly_tick = HourlyTickOrchestrator()
