import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
import argparse
import uvicorn
from packages.config.settings import settings
from packages.logger.logger import logger, audit_log
from database.connection import init_db, AsyncSessionLocal
from database.schema import Channel, Topic, Production, YouTubeVideo
from python.pipelines.hourly_tick import hourly_tick
from python.pipelines.orchestrator import pipeline_orchestrator
from python.services.quota_manager import quota_manager
from python.services.youtube_service import youtube_service
from sqlalchemy.future import select

async def cmd_bootstrap():
    await init_db()
    async with AsyncSessionLocal() as session:
        ch = Channel(
            youtube_channel_id="UC_AUTOPILOT_010",
            title="FutureStack AI Tech",
            niche="AI Tools & Productivity Automation",
            operating_mode=settings.DEFAULT_OPERATING_MODE
        )
        session.add(ch)
        await session.commit()
        logger.info(f"Channel bootstrapped successfully: {ch.title}")

async def cmd_tick():
    await init_db()
    await hourly_tick.run_tick()

async def cmd_dry_run():
    await init_db()
    logger.info("[DRY_RUN] Running first video dry run per Section 76 of BRAIN.md")
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Channel))
        ch = res.scalars().first()
        if not ch:
            ch = Channel(
                youtube_channel_id="UC_DRY_RUN_001",
                title="Dry Run Channel",
                niche="AI Coding Assistants",
                operating_mode="APPROVAL_FIRST"
            )
            session.add(ch)
            await session.commit()
            await session.refresh(ch)

        top = Topic(
            channel_id=ch.id,
            topic="5 New AI Coding Assistants You Never Heard Of",
            score=0.92,
            trend_score=0.92,
            status="SELECTED"
        )
        session.add(top)
        await session.commit()
        await session.refresh(top)

        prod = Production(
            channel_id=ch.id,
            topic_id=top.id,
            status="IDEA",
            format="shorts"
        )
        session.add(prod)
        await session.commit()
        await session.refresh(prod)

        await pipeline_orchestrator.run_production_pipeline(prod.id)
        logger.info(f"[DRY_RUN] Successfully generated dry-run production: {prod.id}")

async def cmd_status():
    await init_db()
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Channel))
        chs = res.scalars().all()
        prods_res = await session.execute(select(Production))
        prods = prods_res.scalars().all()
        print(f"=== YT-AUTOPILOT-X STYTEM STATUS ===")
        print(f"Channels: {len(chs)}")
        print(f"Productions: {len(prods)}")
        print(f"Quota Remaining: {quota_manager.get_remaining_quota()} / 10,000")
        em_status = "ACTIVE" if settings.EMERGENCY_STOP else "OFF"
        print(f"Emergency Stop: {em_status}")

def main():
    parser = argparse.ArgumentParser(
        prog="yt-autopilot",
        description="Autonomous YouTube Channel Operating System"
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("bootstrap", help="Initialize channel and brand identity")
    subparsers.add_parser("run-tick", help="Trigger one hourly autonomous cycle")
    subparsers.add_parser("dry-run", help="Run an end-to-end dry run production")
    subparsers.add_parser("status", help="Display system health and quota")
    subparsers.add_parser("serve", help="Start FastAPI server and dashboard")

    args = parser.parse_args()

    if args.command == "bootstrap":
        asyncio.run(cmd_bootstrap())
    elif args.command == "run-tick":
        asyncio.run(cmd_tick())
    elif args.command == "dry-run":
        asyncio.run(cmd_dry_run())
    elif args.command == "status":
        asyncio.run(cmd_status())
    elif args.command == "serve":
        uvicorn.run("apps.api.main:app", host="0.0.0.0", port=8000, reload=False)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
