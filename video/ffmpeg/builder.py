import os
import subprocess
from typing import List, Optional
import imageio_ffmpeg
from packages.logger.logger import logger

def get_ffmpeg_path() -> str:
    # 1. Check system PATH
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return "ffmpeg"
    except Exception:
        pass
    # 2. Use bundled imageio-ffmpeg binary
    return imageio_ffmpeg.get_ffmpeg_exe()

class FFmpegCommandBuilder:
    def __init__(self):
        self.ffmpeg_path = get_ffmpeg_path()

    def build_scene_command(self, image_path: str, audio_path: str, output_path: str, duration: float, aspect_ratio: str = "9:16") -> List[str]:
        # Always construct command array safely without shell concatenation
        if aspect_ratio == "9:16":
            scale = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
        else:
            scale = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080"

        cmd = [
            self.ffmpeg_path,
            "-y",
            "-loop", "1",
            "-i", image_path,
            "-i", audio_path,
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-vf", scale,
            "-t", str(duration),
            "-shortest",
            output_path
        ]
        return cmd
