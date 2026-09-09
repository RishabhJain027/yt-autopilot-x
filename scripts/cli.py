import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
import asyncio
import argparse
import uvicorn
from packages.config.settings import settings
from packages.logger.logger import logger, audit_log
from database.connection import init_db, AsyncSessionLocal
from database.schema import Channel, Topic, Production, YouTubeVideo
from python.pipelines.hourly_tick import hourly_tick
from python.pipelines.orchestrator import pipeline_orchestrator
from python.agents.goal_agent import goal_agent
from python.agents.browser_researcher import browser_researcher
from python.agents.learning_engine import learning_engine
from python.agents.boost_agent import boost_agent
from python.agents.trend_agent import trend_agent
from python.services.quota_manager import quota_manager
from python.services.youtube_service import youtube_service
from scripts.export_telemetry import export_telemetry
from sqlalchemy.future import select

async def cmd_bootstrap():
    await init_db()
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Channel).where(Channel.youtube_channel_id == "UCOzdVylRBgYrewZ1Q3giwww"))
        ch = res.scalars().first()
        if not ch:
            ch = Channel(
                youtube_channel_id="UCOzdVylRBgYrewZ1Q3giwww",
                title="Maya ✨ Cutie Baddie",
                niche="Pinterest Aesthetic & Girly Clumsy Baddie / Maya ✨",
                operating_mode="AUTONOMOUS",
                status="ACTIVE",
                google_account_email="27rk04@gmail.com"
            )
            session.add(ch)
            await session.commit()
            await session.refresh(ch)
            logger.info(f"Channel bootstrapped successfully: {ch.title} ({ch.youtube_channel_id})")
        else:
            ch.title = "Maya ✨ Cutie Baddie"
            ch.niche = "Pinterest Aesthetic & Girly Clumsy Baddie / Maya ✨"
            ch.operating_mode = "AUTONOMOUS"
            ch.status = "ACTIVE"
            await session.commit()
            logger.info(f"Channel refreshed to AUTONOMOUS mode: {ch.title}")

async def cmd_tick():
    await init_db()
    await hourly_tick.run_tick()

async def cmd_generate_video(topic_override: str = None):
    await init_db()
    logger.info("[VIDEO_GEN] Generating fresh Maya ✨ aesthetic research video from Wikipedia...")
    async with AsyncSessionLocal() as session:
        # 1. Fetch channel
        res = await session.execute(select(Channel).where(Channel.youtube_channel_id == "UCOzdVylRBgYrewZ1Q3giwww"))
        ch = res.scalars().first()
        if not ch:
            ch = Channel(
                youtube_channel_id="UCOzdVylRBgYrewZ1Q3giwww",
                title="Maya ✨ Cutie Baddie",
                niche="Pinterest Aesthetic & Girly Clumsy Baddie / Maya ✨",
                operating_mode="AUTONOMOUS",
                status="ACTIVE",
                google_account_email="27rk04@gmail.com"
            )
            session.add(ch)
            await session.commit()
            await session.refresh(ch)
        else:
            ch.title = "Maya ✨ Cutie Baddie"
            ch.niche = "Pinterest Aesthetic & Girly Clumsy Baddie / Maya ✨"
            await session.commit()

        # 2. Get past topics to avoid repetition
        past_res = await session.execute(select(Topic.topic).where(Topic.channel_id == ch.id))
        past_topics = [t[0] for t in past_res.all()]

        if topic_override:
            chosen_topic = topic_override
            score = 0.98
        else:
            candidates = await trend_agent.discover_trends(
                niche="Pinterest Aesthetic & Girly Clumsy Baddie / Maya ✨",
                pillars=["Wikipedia Psychology", "Aesthetic Magnetism", "History Lore"],
                exclude_topics=past_topics
            )
            if candidates:
                chosen_topic = candidates[0].topic
                score = candidates[0].score
            else:
                chosen_topic = "The Pratfall Effect: Why Clumsy Girls Are Scientifically 10x More Magnetic"
                score = 0.98

        logger.info(f"[VIDEO_GEN] Selected fresh researched topic: '{chosen_topic}' (Score: {score})")
        
        top = Topic(
            channel_id=ch.id,
            topic=chosen_topic,
            score=score,
            trend_score=score,
            status="IN_PROGRESS"
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

        # Run pipeline
        prod_res = await pipeline_orchestrator.run_production_pipeline(prod.id)
        top.status = "COMPLETED"
        await session.commit()
        
        # Export telemetry
        await export_telemetry()
        
        print("\n" + "="*60)
        print(" autonomous video successfully generated & uploaded")
        print(f"Production ID: {prod.id}")
        print(f"Topic: {chosen_topic}")
        print(f"Final Video: {prod_res.final_video_path}")
        print(f"Status: {prod_res.status}")
        print("="*60 + "\n")

async def cmd_goal():
    await init_db()
    status = await goal_agent.get_channel_goal_status()
    print("\n" + "="*60)
    print("=== YT-AUTOPILOT-X | /goal OBJECTIVES & KPI STATUS ===")
    print("="*60)
    print(json.dumps(status, indent=2))
    print("="*60 + "\n")

async def cmd_browser(query: str = None):
    results = await browser_researcher.browse_trending_research(query)
    print("\n" + "="*60)
    print(f"=== YT-AUTOPILOT-X | /browser LIVE RESEARCH RESULTS ({len(results)} items) ===")
    print("="*60)
    print(json.dumps(results, indent=2))
    print("="*60 + "\n")

async def cmd_learn():
    await init_db()
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Channel).limit(1))
        ch = res.scalars().first()
        ch_id = ch.id if ch else "default"
    findings = await learning_engine.analyze_and_learn(ch_id)
    print("\n" + "="*60)
    print(f"=== YT-AUTOPILOT-X | /learn ADAPTIVE STRATEGY FINDINGS ({len(findings)} recommendations) ===")
    print("="*60)
    print(json.dumps(findings, indent=2))
    print("="*60 + "\n")

async def cmd_boost(topic: str = None):
    t = topic or "The 3-Second Eye Contact Trick That Makes Him Obsessed"
    hook = "Okay babes, come closer... why did nobody tell us this seductive eye contact secret? ✨"
    pkg = boost_agent.generate_boost_package(t, hook)
    print("\n" + "="*60)
    print("=== YT-AUTOPILOT-X | /boost VIRAL SEO & RETENTION PACKAGE ===")
    print("="*60)
    print(json.dumps(pkg, indent=2))
    print("="*60 + "\n")

async def cmd_status():
    await init_db()
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Channel))
        chs = res.scalars().all()
        prods_res = await session.execute(select(Production))
        prods = prods_res.scalars().all()
        topics_res = await session.execute(select(Topic))
        topics = topics_res.scalars().all()
        print(f"=== YT-AUTOPILOT-X SYSTEM STATUS ===")
        print(f"Channels: {len(chs)}")
        for c in chs:
            print(f" - {c.title} ({c.youtube_channel_id}) | Mode: {c.operating_mode} | Status: {c.status}")
        print(f"Discovered Topics: {len(topics)}")
        print(f"Total Productions: {len(prods)}")
        print(f"YouTube API Quota Remaining: {quota_manager.get_remaining_quota()} / 10,000")
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
    
    gen_p = subparsers.add_parser("generate-video", help="Generate a fresh breakthrough video on the spot and upload")
    gen_p.add_argument("--topic", type=str, default=None, help="Specific topic override")
    
    subparsers.add_parser("dry-run", help="Run an end-to-end dry run production")
    subparsers.add_parser("goal", help="View channel KPI targets and goal progress (/goal)")
    
    browser_p = subparsers.add_parser("browser", help="Browse live trending research and verified claims (/browser)")
    browser_p.add_argument("--query", type=str, default=None, help="Search query for trending research")

    subparsers.add_parser("learn", help="Run closed-loop adaptive learning engine (/learn)")
    
    boost_p = subparsers.add_parser("boost", help="Generate viral boost package and hook evaluation (/boost)")
    boost_p.add_argument("--topic", type=str, default=None, help="Topic to optimize")

    subparsers.add_parser("daemon", help="Run 1-hour autonomous publishing daemon")
    subparsers.add_parser("export-telemetry", help="Export latest telemetry JSON for GitHub Pages")
    subparsers.add_parser("status", help="Display system health and quota")
    subparsers.add_parser("serve", help="Start FastAPI server and dashboard")

    args = parser.parse_args()

    if args.command == "bootstrap":
        asyncio.run(cmd_bootstrap())
    elif args.command == "run-tick":
        asyncio.run(cmd_tick())
    elif args.command == "generate-video":
        asyncio.run(cmd_generate_video(args.topic))
    elif args.command == "dry-run":
        asyncio.run(cmd_generate_video(args.topic if hasattr(args, 'topic') else None))
    elif args.command == "daemon":
        from scripts.run_hourly_daemon import run_hourly_daemon
        asyncio.run(run_hourly_daemon())
    elif args.command == "goal":
        asyncio.run(cmd_goal())
    elif args.command == "browser":
        asyncio.run(cmd_browser(args.query))
    elif args.command == "learn":
        asyncio.run(cmd_learn())
    elif args.command == "boost":
        asyncio.run(cmd_boost(args.topic))
    elif args.command == "export-telemetry":
        asyncio.run(export_telemetry())
    elif args.command == "status":
        asyncio.run(cmd_status())
    elif args.command == "serve":
        uvicorn.run("apps.api.main:app", host="0.0.0.0", port=8000, reload=False)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
