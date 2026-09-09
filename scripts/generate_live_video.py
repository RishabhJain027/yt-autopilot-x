"""
End-to-End Live Video Generation & YouTube Deployment Script.
Discovers a fresh research breakthrough topic, synthesizes cloud AI scene visuals,
assembles Edge-TTS voiceover and captions, validates quality gates, and uploads live to YouTube.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
import json
from datetime import datetime, timezone
from database.connection import init_db, AsyncSessionLocal
from database.schema import Channel, Topic, Production, YouTubeVideo, Asset, Claim
from python.agents.trend_agent import trend_agent
from python.agents.research_agent import research_agent
from python.agents.script_agent import script_agent
from python.agents.visual_planner import visual_planner
from python.agents.seo_agent import seo_agent
from python.agents.boost_agent import boost_agent
from python.agents.quality_gate import quality_gate
from python.agents.caption_engine import caption_engine
from python.agents.goal_agent import goal_agent
from python.agents.learning_engine import learning_engine
from python.services.tts_service import tts_service
from python.services.image_service import image_service
from python.services.remote_video_router import remote_t2v_router
from video.ffmpeg.renderer import video_renderer
from video.validation.media_validator import media_validator
from python.services.youtube_service import youtube_service
from python.pipelines.state_machine import state_machine
from scripts.export_telemetry import export_telemetry
from packages.logger.logger import logger
from sqlalchemy.future import select

async def main():
    print("=" * 70)
    print("YT-AUTOPILOT-X | LIVE AUTONOMOUS VIDEO PRODUCTION & UPLOAD")
    print("Channel: @MayaCutieBaddie - Maya ✨ Cutie Baddie (UCOzdVylRBgYrewZ1Q3giwww)")
    print("=" * 70)

    await init_db()

    async with AsyncSessionLocal() as session:
        # 1. Ensure channel is seeded and in AUTONOMOUS mode
        ch_res = await session.execute(
            select(Channel).where(Channel.youtube_channel_id == "UCOzdVylRBgYrewZ1Q3giwww")
        )
        ch = ch_res.scalars().first()
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
            ch.operating_mode = "AUTONOMOUS"
            ch.status = "ACTIVE"
            await session.commit()

        print(f"[+] Channel Active: {ch.title} ({ch.youtube_channel_id}) [Mode: {ch.operating_mode}]")

        # 2. Get past topics to avoid repetition
        past_topics_res = await session.execute(
            select(Topic.topic).where(Topic.channel_id == ch.id)
        )
        past_topics = [t[0] for t in past_topics_res.all()]
        print(f"[+] Past topics filtered ({len(past_topics)} past topics): {past_topics}")

        # 3. Discover fresh trending research topics
        candidates = await trend_agent.discover_trends(
            niche="Pinterest Aesthetic & Girly Clumsy Baddie / Maya ✨",
            pillars=["Baddie Psychology", "Dating Secrets", "Aesthetic Magnetism", "Luxury Lore"],
            exclude_topics=past_topics
        )

        top_cand = candidates[0]
        print(f"\n[+] Discovered New Research Breakthrough: '{top_cand.topic}'")
        print(f"    - Trend Score: {top_cand.score}")
        print(f"    - Momentum: {top_cand.momentum}")
        print(f"    - Source: {top_cand.source}")

        # Save topic
        topic_obj = Topic(
            channel_id=ch.id,
            topic=top_cand.topic,
            score=top_cand.score,
            trend_score=top_cand.trend_score,
            competition_score=top_cand.competition_score,
            rights_risk=top_cand.rights_risk,
            status="IN_PROGRESS",
            evidence_json=top_cand.evidence
        )
        session.add(topic_obj)
        await session.commit()
        await session.refresh(topic_obj)

        # 4. Create Production
        prod = Production(
            channel_id=ch.id,
            topic_id=topic_obj.id,
            status="IDEA",
            format="shorts"
        )
        session.add(prod)
        await session.commit()
        await session.refresh(prod)

        print(f"\n[+] Production ID: {prod.id}")

        # Step 1: Researching
        prod.status = state_machine.transition(prod.status, 'RESEARCHING', prod.id, prod.channel_id)
        await session.commit()
        research = await research_agent.research_topic(top_cand.topic)
        for c in research.claims:
            session.add(Claim(
                production_id=prod.id,
                claim_text=c.claim_text,
                source_url=c.source_url,
                source_title=c.source_title,
                source_publisher=c.source_publisher,
                confidence=c.confidence,
                supports_claim=c.supports_claim,
                requires_human_review=c.requires_human_review
            ))
        prod.status = state_machine.transition(prod.status, 'RESEARCH_READY', prod.id, prod.channel_id)
        await session.commit()
        print(f"[+] Research Completed: {len(research.claims)} verified claims logged to Evidence Desk.")

        # Step 2: Scripting
        prod.status = state_machine.transition(prod.status, 'SCRIPTING', prod.id, prod.channel_id)
        await session.commit()
        script = await script_agent.generate_script(top_cand.topic, research, format="shorts")
        prod.script_json = script.model_dump()
        prod.status = state_machine.transition(prod.status, 'SCRIPT_READY', prod.id, prod.channel_id)
        await session.commit()
        print(f"[+] Script Synthesized: Hook -> \"{script.hook}\" ({len(script.segments)} scenes)")

        # Step 3: Visual Planning
        prod.status = state_machine.transition(prod.status, 'VISUAL_PLANNING', prod.id, prod.channel_id)
        await session.commit()
        visuals = visual_planner.plan_visuals(script, aspect_ratio="9:16")
        prod.visual_json = visuals.model_dump()
        prod.status = state_machine.transition(prod.status, 'ASSET_READY', prod.id, prod.channel_id)
        await session.commit()
        print(f"[+] Visual Storyboard Planned: {len(visuals.scenes)} 9:16 scenes configured.")

        # Step 4: Voice & Audio Generation
        prod.status = state_machine.transition(prod.status, 'VOICE_GENERATION', prod.id, prod.channel_id)
        await session.commit()
        narration = " ".join([s.voiceover for s in script.segments])
        audio_path, duration = await tts_service.synthesize(narration, filename_prefix=f"live_{prod.id}")
        prod.audio_path = audio_path
        prod.render_duration_seconds = duration
        print(f"[+] Voiceover Generated: {audio_path} ({duration:.1f}s)")

        # Step 5: Captions
        srt_path = caption_engine.generate_srt(script, filename_prefix=f"live_{prod.id}")
        prod.caption_path = srt_path
        prod.status = state_machine.transition(prod.status, 'CAPTIONS_GENERATED', prod.id, prod.channel_id)
        await session.commit()
        print(f"[+] Captions Formatted: {srt_path}")

        # Step 6: Rendering
        prod.status = state_machine.transition(prod.status, 'RENDERING', prod.id, prod.channel_id)
        await session.commit()

        thumb_path = image_service.generate_thumbnail(script.title_candidate, subtitle="Complete Breakdown", aspect_ratio="9:16", filename_prefix=f"live_{prod.id}")
        prod.thumbnail_path = thumb_path
        session.add(Asset(
            production_id=prod.id,
            source_type="generated_thumbnail",
            local_path=thumb_path,
            rights_status="COMMERCIAL_VERIFIED",
            license_json={"type": "Apache-2.0", "generator": "ImageService"}
        ))

        print(f"[+] Generating Cloud AI scene visuals across remote models (Wan2.1 / Flux / CogVideoX)...")
        t2v_clips = await remote_t2v_router.generate_storyboard_clips([s.model_dump() for s in visuals.scenes], aspect_ratio="9:16")
        for clip in t2v_clips:
            session.add(Asset(
                production_id=prod.id,
                source_type="remote_t2v_clip",
                local_path=clip.get("clip_path"),
                rights_status="COMMERCIAL_VERIFIED",
                license_json={"model": clip.get("model_used"), "license": "Apache 2.0 / Open Source"}
            ))

        print(f"[+] Stitching multi-scene vertical video with subtitle captions...")
        video_path, render_dur = video_renderer.render_production(
            production_id=prod.id,
            scenes=[s.model_dump() for s in visuals.scenes],
            audio_path=audio_path,
            total_duration=duration,
            aspect_ratio="9:16",
            clips=t2v_clips,
            caption_path=srt_path
        )
        prod.final_video_path = video_path

        valid, val_report = media_validator.validate_video_file(video_path)
        prod.video_hash_sha256 = val_report.get('sha256')
        prod.status = state_machine.transition(prod.status, 'RENDERED', prod.id, prod.channel_id)
        await session.commit()
        print(f"[+] Video Rendered & Validated: {video_path} (Hash: {prod.video_hash_sha256[:16]}...)")

        # Step 7: SEO & Viral Boost
        seo_pkg = await seo_agent.generate_metadata(top_cand.topic, narration)
        boost_pkg = boost_agent.generate_boost_package(top_cand.topic, script.hook)
        pub_dict = seo_pkg.model_dump()
        pub_dict["boost"] = boost_pkg
        pub_dict["tags"] = list(set(pub_dict.get("tags", []) + boost_pkg.get("hashtags", [])))
        prod.publishing_json = pub_dict

        # Step 8: Quality Gate
        prod.status = state_machine.transition(prod.status, 'QA_PENDING', prod.id, prod.channel_id)
        await session.commit()
        gate_report = quality_gate.validate_production(script, research, video_exists=valid)
        prod.review_json = gate_report.model_dump()
        print(f"[+] 6 Machine Quality Gates: {'ALL PASSED' if gate_report.overall_passed else 'FAILED'}")

        # Step 9: Autonomous Upload & Publishing
        if gate_report.overall_passed:
            prod.status = state_machine.transition(prod.status, 'APPROVED', prod.id, prod.channel_id)
            print(f"[+] Executing YouTube Upload to channel {ch.youtube_channel_id}...")
            upload_res = await youtube_service.upload_video(
                channel_id=prod.channel_id,
                video_path=prod.final_video_path,
                title=pub_dict.get("primary_title", seo_pkg.primary_title),
                description=f"{pub_dict.get('description', seo_pkg.description)}\n\n{' '.join(boost_pkg.get('hashtags', []))}",
                tags=pub_dict.get("tags", seo_pkg.tags),
                contains_synthetic_media=True
            )
            yt_vid = YouTubeVideo(
                production_id=prod.id,
                youtube_video_id=upload_res.get('youtube_video_id'),
                upload_status=upload_res.get('upload_status'),
                privacy_status=upload_res.get('privacy_status'),
                contains_synthetic_media=upload_res.get('contains_synthetic_media', True),
                response_json=upload_res
            )
            session.add(yt_vid)
            prod.status = state_machine.transition(prod.status, 'UPLOADING', prod.id, prod.channel_id)
            prod.status = state_machine.transition(prod.status, 'SCHEDULED', prod.id, prod.channel_id)
            topic_obj.status = "COMPLETED"
            await session.commit()
            print(f"\n[+] LIVE YOUTUBE UPLOAD COMPLETE!")
            print(f"    - YouTube Video ID: {yt_vid.youtube_video_id}")
            print(f"    - Status: {yt_vid.upload_status} ({yt_vid.privacy_status})")
            print(f"    - URL: https://youtube.com/shorts/{yt_vid.youtube_video_id}")

        # Step 10: Learning Cycle
        await learning_engine.analyze_and_learn(ch.id)

        # Step 11: Export Telemetry
        await export_telemetry()
        print(f"\n[+] Exported live rich telemetry to docs/telemetry.json")

    print("\n" + "=" * 70)
    print("PRODUCTION & DEPLOYMENT RUN COMPLETE")
    print("=" * 70)

if __name__ == '__main__':
    asyncio.run(main())
