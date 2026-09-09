import asyncio
import os
import sys
from datetime import datetime, timezone
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import AsyncSessionLocal, init_db
from database.schema import Channel, Production, YouTubeVideo, Topic
from python.services.quota_manager import quota_manager
from python.services.youtube_service import youtube_service
from python.pipelines.state_machine import state_machine
from scripts.export_telemetry import export_telemetry
from sqlalchemy.future import select

async def main():
    await init_db()
    quota_manager.reset_quota()
    print("Quota reset to 0/10000.")

    async with AsyncSessionLocal() as session:
        # Find latest rendered production
        res = await session.execute(
            select(Production).where(Production.id == "6107f8e6-90a7-4138-aca8-6f158bc464bb")
        )
        prod = res.scalars().first()
        if not prod:
            print("Production 6107f8e6-90a7-4138-aca8-6f158bc464bb not found.")
            return

        print(f"Found production: {prod.id}, status: {prod.status}, video: {prod.final_video_path}")
        
        # Ensure video exists
        if not os.path.exists(prod.final_video_path):
            print(f"Error: Final video path not found: {prod.final_video_path}")
            return

        pub_dict = prod.publishing_json or {}
        boost_pkg = pub_dict.get("boost", {})
        title = pub_dict.get("primary_title", "The Open Source AI Revolution Nobody is Talking About")
        description = f"{pub_dict.get('description', 'Discover the silent open source AI models breaking closed-source dominance.')}\n\n{' '.join(boost_pkg.get('hashtags', ['#AI', '#OpenSourceAI', '#TechShorts']))}"
        tags = pub_dict.get("tags", ["AI", "OpenSourceAI", "Wan21", "MachineLearning", "Shorts"])

        # Upload
        print(f"Uploading video '{title}' for channel {prod.channel_id}...")
        upload_res = await youtube_service.upload_video(
            channel_id=prod.channel_id,
            video_path=prod.final_video_path,
            title=title,
            description=description,
            tags=tags,
            contains_synthetic_media=True
        )

        print(f"Upload result: {upload_res}")

        yt_vid = YouTubeVideo(
            production_id=prod.id,
            youtube_video_id=upload_res.get('youtube_video_id'),
            upload_status=upload_res.get('upload_status'),
            privacy_status=upload_res.get('privacy_status'),
            contains_synthetic_media=upload_res.get('contains_synthetic_media', True),
            response_json=upload_res
        )
        session.add(yt_vid)
        
        prod.status = "SCHEDULED"
        
        # Mark topic completed
        top_res = await session.execute(select(Topic).where(Topic.id == prod.topic_id))
        top = top_res.scalars().first()
        if top:
            top.status = "COMPLETED"

        await session.commit()
        print(f"Production {prod.id} successfully updated to SCHEDULED/UPLOADED!")

    await export_telemetry()
    print("Telemetry exported successfully.")

if __name__ == "__main__":
    asyncio.run(main())
