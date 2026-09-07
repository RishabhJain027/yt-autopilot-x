import os
import subprocess
import tempfile
from typing import List, Dict, Any, Tuple
from PIL import Image, ImageDraw
import imageio_ffmpeg
from packages.config.settings import settings
from packages.logger.logger import logger
from video.ffmpeg.builder import FFmpegCommandBuilder, get_ffmpeg_path

class VideoRenderer:
    def __init__(self):
        self.builder = FFmpegCommandBuilder()
        self.renders_dir = os.path.join(settings.STORAGE_ROOT, "renders")
        os.makedirs(self.renders_dir, exist_ok=True)

    def render_production(self, production_id: str, scenes: List[Dict[str, Any]], audio_path: str, total_duration: float, aspect_ratio: str = "9:16") -> Tuple[str, float]:
        output_path = os.path.join(self.renders_dir, f"prod_{production_id}_final.mp4")
        
        # 1. Create visually rich title slide/card
        width, height = (1080, 1920) if aspect_ratio == "9:16" else (1920, 1080)
        scene_img_path = os.path.join(settings.STORAGE_ROOT, "scenes", f"{production_id}_slide.png")
        os.makedirs(os.path.dirname(scene_img_path), exist_ok=True)
        
        img = Image.new("RGB", (width, height), color="#090D16")
        draw = ImageDraw.Draw(img)
        
        # Draw background grid & futuristic glowing accent bars
        for y in range(0, height, 40):
            draw.line([(0, y), (width, y)], fill="#131B2E", width=1)
        for x in range(0, width, 40):
            draw.line([(x, 0), (x, height)], fill="#131B2E", width=1)
            
        # Draw dynamic color blocks
        draw.rectangle([60, 120, width - 60, height - 120], outline="#38BDF8", width=4)
        draw.rectangle([80, height // 3, width - 80, (height // 3) + 200], fill="#0284C7")
        draw.text((120, 160), "AUTOPILOT-X AUTONOMOUS VIDEO", fill="#F43F5E")
        
        # Text from first scene or production
        prompt_text = scenes[0].get("prompt", "AI Technology Brief")[:80] if scenes else "AI Technology Automation"
        draw.text((120, (height // 3) + 80), prompt_text.upper(), fill="#FFFFFF")
        
        img.save(scene_img_path, format="PNG")

        # 2. Run FFmpeg command safely
        cmd = self.builder.build_scene_command(
            image_path=scene_img_path,
            audio_path=audio_path,
            output_path=output_path,
            duration=max(3.0, total_duration),
            aspect_ratio=aspect_ratio
        )
        
        logger.info(f"[RENDER] Executing FFmpeg command for production {production_id}")
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            logger.error(f"[RENDER] FFmpeg failed with code {res.returncode}: {res.stderr}")
            raise RuntimeError(f"FFmpeg render failed: {res.stderr[:300]}")

        logger.info(f"[RENDER] Final video rendered successfully: {output_path}")
        return output_path, total_duration

video_renderer = VideoRenderer()
