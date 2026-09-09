from datetime import datetime, timezone, timedelta
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
            # 1. Fetch active channels (Prioritize authenticated channels)
            res = await session.execute(select(Channel).where(Channel.status == 'ACTIVE'))
            channels = res.scalars().all()
            if not channels:
                logger.info("[HOURLY_TICK] Initializing default channel @RishabhAIStudio-27...")
                ch = Channel(
                    youtube_channel_id="UCOzdVylRBgYrewZ1Q3giwww",
                    title="Rishabh AI Studio",
                    niche="AI Breakthroughs & Autonomous Dev",
                    operating_mode="AUTONOMOUS",
                    status="ACTIVE",
                    google_account_email="27rk04@gmail.com"
                )
                session.add(ch)
                await session.commit()
                await session.refresh(ch)
                channels = [ch]

            for ch in channels:
                try:
                    logger.info(f"[HOURLY_TICK] Processing channel: {ch.title} ({ch.youtube_channel_id})")

                    # Self-Healing: Clean up stale jobs older than 3 hours stuck in intermediate states
                    stuck_cutoff = datetime.now(timezone.utc) - timedelta(hours=3)
                    stale_prods = await session.execute(
                        select(Production).where(
                            Production.channel_id == ch.id,
                            Production.status.in_(['IDEA', 'RESEARCHING', 'SCRIPTING', 'RENDERING', 'QA_PENDING']),
                            Production.created_at < stuck_cutoff
                        )
                    )
                    for stale in stale_prods.scalars().all():
                        logger.warning(f"[HOURLY_TICK] Auto-clearing stale production {stale.id} (status: {stale.status}) to avoid backpressure deadlock.")
                        stale.status = 'FAILED'
                    await session.commit()

                    # Check Active Backlog
                    pending_prods = await session.execute(
                        select(Production).where(
                            Production.channel_id == ch.id,
                            Production.status.in_(['IDEA', 'RESEARCHING', 'SCRIPTING', 'RENDERING'])
                        )
                    )
                    active_jobs = pending_prods.scalars().all()

                    if len(active_jobs) >= settings.MAX_RENDER_QUEUE:
                        logger.info(f"[HOURLY_TICK] Active rendering queue full ({len(active_jobs)} active jobs). Waiting for current batch to complete.")
                        continue

                    # Retrieve all past topics for anti-repetition filter
                    all_past_topics_res = await session.execute(
                        select(Topic.topic).where(Topic.channel_id == ch.id)
                    )
                    past_topics = [t[0] for t in all_past_topics_res.all()]

                    # Discover new trends & topics if backlog is low
                    topics_res = await session.execute(
                        select(Topic).where(Topic.channel_id == ch.id, Topic.status == 'DISCOVERED')
                    )
                    available_topics = topics_res.scalars().all()

                    if not available_topics:
                        logger.info(f"[HOURLY_TICK] Discovering fresh breakthrough viral trends for {ch.niche or 'AI Tech'} (excluding {len(past_topics)} past topics)...")
                        candidates = await trend_agent.discover_trends(
                            niche=ch.niche or "AI Breakthroughs",
                            pillars=["AI Foundation Models", "Open Source AI", "Autonomous Agents", "Developer Productivity"],
                            exclude_topics=past_topics
                        )
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
                        await session.refresh(prod)

                        logger.info(f"[HOURLY_TICK] Launched production {prod.id} for topic: '{top_topic.topic}'")
                        # Run production pipeline
                        try:
                            await pipeline_orchestrator.run_production_pipeline(prod.id)
                            top_topic.status = 'COMPLETED'
                            await session.commit()
                            logger.info(f"[HOURLY_TICK] Successfully completed production pipeline for {prod.id}")
                        except Exception as pe:
                            logger.error(f"[HOURLY_TICK] Pipeline failed for production {prod.id}: {pe}")
                            prod.status = 'FAILED'
                            top_topic.status = 'DISCOVERED'
                            await session.commit()
                except Exception as ce:
                    logger.error(f"[HOURLY_TICK] Error processing channel {ch.title}: {ce}")

        # Export updated telemetry for GitHub Pages dashboard
        try:
            from scripts.export_telemetry import export_telemetry
            await export_telemetry()
        except Exception as te:
            logger.warning(f"[HOURLY_TICK] Telemetry export note: {te}")

        logger.info("[HOURLY_TICK] === Autonomous cycle complete ===")

hourly_tick = HourlyTickOrchestrator()
