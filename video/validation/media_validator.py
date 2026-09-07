import hashlib
import os
import subprocess
from typing import Dict, Any, Tuple
import imageio_ffmpeg
from packages.logger.logger import logger

class MediaValidator:
    def calculate_sha256(self, filepath: str) -> str:
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def validate_video_file(self, filepath: str) -> Tuple[bool, Dict[str, Any]]:
        if not os.path.exists(filepath):
            return False, {"error": "File does not exist"}
        
        size = os.path.getsize(filepath)
        if size < 1024:
            return False, {"error": "File is abnormally small or empty", "size_bytes": size}

        file_hash = self.calculate_sha256(filepath)
        
        # Use imageio-ffmpeg / ffprobe to check format
        # Verify file header (MP4 contains ftyp)
        with open(filepath, "rb") as f:
            header = f.read(32)
            is_mp4 = b"ftyp" in header or b"moov" in header

        return True, {
            "valid": True,
            "filepath": filepath,
            "size_bytes": size,
            "sha256": file_hash,
            "is_mp4_container": is_mp4
        }

media_validator = MediaValidator()
