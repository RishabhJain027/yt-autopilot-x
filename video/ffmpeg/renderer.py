import os
import subprocess
import tempfile
from typing import List, Dict, Any, Tuple, Optional
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

    def render_production(self, production_id: str, scenes: List[Dict[str, Any]], audio_path: str, total_duration: float, aspect_ratio: str = "9:16", clips: Optional[List[Dict[str, Any]]] = None) -> Tuple[str, float]:
        output_path = os.path.join(self.renders_dir, f"prod_{production_id}_final.mp4")
        width, height = (1080, 1920) if aspect_ratio == "9:16" else (1920, 1080)
        ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()

        valid_clip_paths = []
        if clips:
            for c in clips:
                p = c.get("clip_path")
                if p and os.path.exists(p):
                    valid_clip_paths.append(p)

        # 1. Multi-Clip Text-to-Video Stitching Mode
        if valid_clip_paths and len(valid_clip_paths) > 0:
            logger.info(f"[RENDER] Stitching {len(valid_clip_paths)} remote T2V AI video clips for production {production_id}...")
            concat_txt_path = os.path.join(settings.STORAGE_ROOT, "renders", f"concat_{production_id}.txt")
            with open(concat_txt_path, "w", encoding="utf-8") as f:
                for cp in valid_clip_paths:
                    # Windows paths need forward slashes or escaping for FFmpeg concat demuxer
                    clean_p = os.path.abspath(cp).replace("\\", "/")
                    f.write(f"file '{clean_p}'\n")

            cmd = [
                ffmpeg_bin, "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", concat_txt_path,
                "-i", audio_path,
                "-vf", f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},setsar=1",
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "20",
                "-c:a", "aac",
                "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-shortest",
                output_path
            ]

            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0:
                logger.info(f"[RENDER] Final multi-clip AI video rendered successfully: {output_path}")
                return output_path, total_duration
            else:
                logger.warning(f"[RENDER] Concat failed ({res.stderr[:200]}), falling back to procedural title sequence.")

        # 2. Procedural Fallback Title Visual Animation
        scene_img_path = os.path.join(settings.STORAGE_ROOT, "scenes", f"{production_id}_slide.png")
        os.makedirs(os.path.dirname(scene_img_path), exist_ok=True)
        
        img = Image.new("RGB", (width, height), color="#090D16")
        draw = ImageDraw.Draw(img)
        
        for y in range(0, height, 40):
            draw.line([(0, y), (width, y)], fill="#131B2E", width=1)
        for x in range(0, width, 40):
            draw.line([(x, 0), (x, height)], fill="#131B2E", width=1)
            
        draw.rectangle([60, 120, width - 60, height - 120], outline="#38BDF8", width=4)
        draw.rectangle([80, height // 3, width - 80, (height // 3) + 200], fill="#0284C7")
        draw.text((120, 160), "WAN2.1 / COGVIDEOX POWERED", fill="#F43F5E")
        
        prompt_text = scenes[0].get("prompt", "AI Technology Brief")[:80] if scenes else "AI Technology Automation"
        draw.text((120, (height // 3) + 80), prompt_text.upper(), fill="#FFFFFF")
        
        img.save(scene_img_path, format="PNG")

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
