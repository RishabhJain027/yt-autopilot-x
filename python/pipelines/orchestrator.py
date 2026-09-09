import os
import json
from datetime import datetime, timezone
from sqlalchemy.future import select
from database.connection import AsyncSessionLocal
from database.schema import Channel, Topic, Production, Claim, Asset, YouTubeVideo, ReviewRecord
from python.pipelines.state_machine import state_machine
from python.agents.research_agent import research_agent
from python.agents.script_agent import script_agent
from python.agents.visual_planner import visual_planner
from python.agents.seo_agent import seo_agent
from python.agents.boost_agent import boost_agent
from python.agents.quality_gate import quality_gate
from python.agents.caption_engine import caption_engine
from python.services.tts_service import tts_service
from python.services.image_service import image_service
from video.ffmpeg.renderer import video_renderer
from video.validation.media_validator import media_validator
from python.services.youtube_service import youtube_service
from python.services.remote_video_router import remote_t2v_router
from python.schemas.rights import AssetProvenance
from packages.config.settings import settings
from packages.logger.logger import logger, audit_log

class PipelineOrchestrator:
    async def run_production_pipeline(self, production_id: str) -> Production:
        async with AsyncSessionLocal() as session:
            # 1. Load production
            result = await session.execute(select(Production).where(Production.id == production_id))
            prod = result.scalar_one_or_none()
            if not prod:
                raise ValueError(f"Production {production_id} not found")

            topic_title = "AI Video & Technology Automation"
            if prod.topic_id:
                top_res = await session.execute(select(Topic).where(Topic.id == prod.topic_id))
                topic_obj = top_res.scalar_one_or_none()
                if topic_obj:
                    topic_title = topic_obj.topic

            # Fetch channel & niche
            ch_res = await session.execute(select(Channel).where(Channel.id == prod.channel_id))
            channel_obj = ch_res.scalar_one_or_none()
            channel_niche = channel_obj.niche if (channel_obj and channel_obj.niche) else settings.DEFAULT_NICHE

            # Step 1: Researching
            prod.status = state_machine.transition(prod.status, 'RESEARCHING', prod.id, prod.channel_id)
            await session.commit()
            research = await research_agent.research_topic(topic_title)
            
            # Save claims
            for claim_data in research.claims:
                claim = Claim(
                    production_id=prod.id,
                    claim_text=claim_data.claim_text,
                    source_url=claim_data.source_url,
                    source_title=claim_data.source_title,
                    source_publisher=claim_data.source_publisher,
                    confidence=claim_data.confidence,
                    supports_claim=claim_data.supports_claim,
                    requires_human_review=claim_data.requires_human_review
                )
                session.add(claim)

            prod.status = state_machine.transition(prod.status, 'RESEARCH_READY', prod.id, prod.channel_id)
            await session.commit()

            # Step 2: Scripting (Niche-Aware Viral Storyboard)
            prod.status = state_machine.transition(prod.status, 'SCRIPTING', prod.id, prod.channel_id)
            await session.commit()
            script = await script_agent.generate_script(topic_title, research, format=prod.format, niche=channel_niche)
            prod.script_json = script.model_dump()
            prod.status = state_machine.transition(prod.status, 'SCRIPT_READY', prod.id, prod.channel_id)
            await session.commit()

            # Step 3: Visual Planning (Character Consistency & Clean Rendering)
            prod.status = state_machine.transition(prod.status, 'VISUAL_PLANNING', prod.id, prod.channel_id)
            await session.commit()
            aspect_ratio = "9:16" if prod.format == "shorts" else "16:9"
            visuals = visual_planner.plan_visuals(script, aspect_ratio=aspect_ratio, niche=channel_niche)
            prod.visual_json = visuals.model_dump()
            prod.status = state_machine.transition(prod.status, 'ASSET_READY', prod.id, prod.channel_id)
            await session.commit()

            # Step 4: Voice & Audio Generation (Multi-Persona TTS voiceover)
            prod.status = state_machine.transition(prod.status, 'VOICE_GENERATION', prod.id, prod.channel_id)
            await session.commit()
            narration_full = " ".join([seg.voiceover for seg in script.segments])
            audio_path, duration = await tts_service.synthesize(narration_full, niche=channel_niche, filename_prefix=f"prod_{prod.id}")
            prod.audio_path = audio_path
            prod.render_duration_seconds = duration

            # Step 5: Caption Engine
            srt_path = caption_engine.generate_srt(script, filename_prefix=f"prod_{prod.id}")
            prod.caption_path = srt_path
            prod.status = state_machine.transition(prod.status, 'CAPTIONS_GENERATED', prod.id, prod.channel_id)
            await session.commit()

            # Step 6: Rendering & Thumbnail Generation
            prod.status = state_machine.transition(prod.status, 'RENDERING', prod.id, prod.channel_id)
            await session.commit()
            
            # Generate thumbnail
            thumb_path = image_service.generate_thumbnail(script.title_candidate, subtitle="Complete Blueprint", aspect_ratio=aspect_ratio, filename_prefix=f"prod_{prod.id}")
            prod.thumbnail_path = thumb_path

            # Asset ledger: Add thumbnail asset
            session.add(Asset(
                production_id=prod.id,
                source_type="generated_thumbnail",
                local_path=thumb_path,
                rights_status="COMMERCIAL_VERIFIED",
                license_json={"type": "Apache-2.0", "generator": "ImageService"}
            ))

            # Generate remote serverless T2V clips across foundation model fleet (Wan 2.2 / HunyuanVideo 1.5 / LTX-2.5 / Flux)
            t2v_clips = await remote_t2v_router.generate_storyboard_clips([s.model_dump() for s in visuals.scenes], aspect_ratio=aspect_ratio, niche=channel_niche)

            # Asset ledger: Add clip assets
            for clip in t2v_clips:
                session.add(Asset(
                    production_id=prod.id,
                    source_type="remote_t2v_clip",
                    local_path=clip.get("clip_path"),
                    rights_status="COMMERCIAL_VERIFIED",
                    license_json={"model": clip.get("model_used"), "license": "Apache 2.0 / Open Source"}
                ))

            # Render multi-clip video with subtitle captions
            video_path, render_dur = video_renderer.render_production(
                production_id=prod.id,
                scenes=[s.model_dump() for s in visuals.scenes],
                audio_path=audio_path,
                total_duration=duration,
                aspect_ratio=aspect_ratio,
                clips=t2v_clips,
                caption_path=srt_path
            )
            prod.final_video_path = video_path

            # Validate video
            valid, val_report = media_validator.validate_video_file(video_path)
            prod.video_hash_sha256 = val_report.get('sha256')
            prod.status = state_machine.transition(prod.status, 'RENDERED', prod.id, prod.channel_id)
            await session.commit()

            # Step 7: SEO & Viral Boost Packaging
            seo_pkg = await seo_agent.generate_metadata(topic_title, narration_full)
            boost_pkg = boost_agent.generate_boost_package(topic_title, script.hook, category=channel_niche)
            
            # Merge boost attributes into publishing JSON
            pub_dict = seo_pkg.model_dump()
            pub_dict["boost"] = boost_pkg
            pub_dict["tags"] = list(set(pub_dict.get("tags", []) + boost_pkg.get("hashtags", [])))
            prod.publishing_json = pub_dict

            # Step 8: Quality & Policy Gate
            prod.status = state_machine.transition(prod.status, 'QA_PENDING', prod.id, prod.channel_id)
            await session.commit()
            gate_report = quality_gate.validate_production(script, research, video_exists=valid)
            prod.review_json = gate_report.model_dump()

            # Step 9: Autonomy / Review Determination
            is_autonomous = (channel_obj and channel_obj.operating_mode == 'AUTONOMOUS') or settings.AUTONOMOUS_PUBLISHING
            if gate_report.overall_passed and is_autonomous:
                prod.status = state_machine.transition(prod.status, 'APPROVED', prod.id, prod.channel_id)
                # Auto Upload to YouTube
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
            else:
                # Approval-first mode: send to Review Studio
                prod.status = state_machine.transition(prod.status, 'REVIEW_PENDING', prod.id, prod.channel_id)
                rev = ReviewRecord(
                    production_id=prod.id,
                    reviewer_id='operator',
                    feedback_notes='Awaiting human approval in Review Studio.'
                )
                session.add(rev)

            await session.commit()
            return prod

pipeline_orchestrator = PipelineOrchestrator()
