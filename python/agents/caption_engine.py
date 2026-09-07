import os
from typing import List, Dict, Any
from packages.config.settings import settings
from python.schemas.script import ScriptPlan

class CaptionEngine:
    def __init__(self):
        self.output_dir = os.path.join(settings.STORAGE_ROOT, 'captions')
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_srt(self, script: ScriptPlan, filename_prefix: str = 'sub') -> str:
        srt_path = os.path.join(self.output_dir, f'{filename_prefix}_{int(abs(hash(script.hook)))}.srt')
        lines = []
        current_time = 0.0

        for idx, seg in enumerate(script.segments, 1):
            start_sec = current_time
            end_sec = current_time + seg.duration
            current_time = end_sec

            # Format SRT time 00:00:00,000
            start_str = self._format_srt_time(start_sec)
            end_str = self._format_srt_time(end_sec)

            lines.append(f"{idx}")
            lines.append(f"{start_str} --> {end_str}")
            lines.append(seg.voiceover.strip())
            lines.append("")

        with open(srt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        return srt_path

    def _format_srt_time(self, seconds: float) -> str:
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

caption_engine = CaptionEngine()
