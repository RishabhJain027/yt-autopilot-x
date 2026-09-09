"""
SexyVoice.ai Integration Module.
Integrates all English Female Seductive Voices from https://github.com/gianpaj/sexyvoice.git:
- Gemini 2.5 / 3.1 Pro: Aoede (Deep Sultry), Kore (Sensual Whisper), Zephyr (Playful Magnetic)
- xAI Grok: Eve (Commanding Playful Baddie), Ara (Soft Affectionate Whisper)
- Neural Flagship: en-US-AvaNeural (Deep Breathy Velvet), en-US-JennyNeural, en-US-EmmaNeural, en-GB-SoniaNeural (Luxury British)

Includes:
1. Speech Tags Parser ([pause], [long-pause], [giggle], [sigh], [breath], <whisper>, <soft>, <slow>, <lower-pitch>)
2. SSML Prosody & Pacing Optimizer for Seductive Delivery
3. High-End Studio Acoustic DSP Chain (Chest Resonance, Proximity Compression, Air Silkiness)
"""

import os
import re
import math
import subprocess
import asyncio
from typing import Dict, Any, Optional, Tuple, List
from packages.config.settings import settings
from packages.logger.logger import logger, audit_log

class SexyVoiceRegistry:
    """
    Catalog of all English Female Voices extracted from SexyVoice.ai repository.
    """
    VOICES: Dict[str, Dict[str, Any]] = {
        "aoede": {
            "name": "Aoede",
            "provider": "gemini",
            "model": "gpro31",
            "gender": "Female",
            "language": "en",
            "tone": "Deep, sultry, rich feminine voice with velvety vocal fry",
            "style_prompt": "Extremely seductive, deep, velvety, whispery, intimate baddie voice with alluring vocal fry and slow magnetic pacing."
        },
        "kore": {
            "name": "Kore",
            "provider": "gemini",
            "model": "gpro",
            "gender": "Female",
            "language": "en",
            "tone": "Sensual, whispery, breathy intimate feminine voice",
            "style_prompt": "Sensual, soft, breathy whispery tone, speaking intimately close to the microphone."
        },
        "zephyr": {
            "name": "Zephyr",
            "provider": "gemini",
            "model": "gpro",
            "gender": "Female",
            "language": "en",
            "tone": "Playful, magnetic, teasing aesthetic baddie voice",
            "style_prompt": "Playful, teasing, vibrant yet alluringly seductive and charming."
        },
        "eve": {
            "name": "Eve",
            "provider": "xai",
            "model": "xai",
            "gender": "Female",
            "language": "en",
            "tone": "Confident, commanding, playful female seductive voice with expressive speech tags",
            "speech_tags_enabled": True
        },
        "ara": {
            "name": "Ara",
            "provider": "xai",
            "model": "xai",
            "gender": "Female",
            "language": "en",
            "tone": "Soft-spoken, affectionate, whispery seductive female voice",
            "speech_tags_enabled": True
        },
        "ava_seductive": {
            "name": "en-US-AvaNeural",
            "provider": "edge_neural",
            "model": "neural",
            "gender": "Female",
            "language": "en-US",
            "tone": "Ultra-seductive, deep, breathy, velvety intimate bedroom voice",
            "rate": "-8%",
            "pitch": "-3Hz",
            "volume": "+15%"
        },
        "jenny_alluring": {
            "name": "en-US-JennyNeural",
            "provider": "edge_neural",
            "model": "neural",
            "gender": "Female",
            "language": "en-US",
            "tone": "Warm, expressive, alluring feminine tone",
            "rate": "-6%",
            "pitch": "-2Hz",
            "volume": "+12%"
        },
        "emma_velvet": {
            "name": "en-US-EmmaNeural",
            "provider": "edge_neural",
            "model": "neural",
            "gender": "Female",
            "language": "en-US",
            "tone": "Rich, velvety, clear seductive broadcast tone",
            "rate": "-7%",
            "pitch": "-2Hz",
            "volume": "+12%"
        },
        "sonia_luxury": {
            "name": "en-GB-SoniaNeural",
            "provider": "edge_neural",
            "model": "neural",
            "gender": "Female",
            "language": "en-GB",
            "tone": "Sophisticated, posh, sultry Upper East Side / British luxury tone",
            "rate": "-6%",
            "pitch": "-1Hz",
            "volume": "+10%"
        }
    }

class SexyVoiceEngine:
    def __init__(self):
        self.output_dir = os.path.join(settings.STORAGE_ROOT, "audio")
        os.makedirs(self.output_dir, exist_ok=True)
        self.registry = SexyVoiceRegistry()

    def parse_speech_tags_to_ssml(self, text: str, voice_name: str = "en-US-AvaNeural") -> str:
        """
        Parses SexyVoice speech tags ([pause], [sigh], <whisper>, <soft>, etc.)
        into standard SSML for deep emotional, seductive prosody.
        """
        parsed = text
        # Instant tags
        parsed = parsed.replace("[pause]", '<break time="350ms"/>')
        parsed = parsed.replace("[long-pause]", '<break time="650ms"/>')
        parsed = parsed.replace("[breath]", '<break time="200ms"/>')
        parsed = parsed.replace("[sigh]", '<break time="300ms"/>')
        parsed = parsed.replace("[giggle]", '<break time="250ms"/>')
        parsed = parsed.replace("[chuckle]", '<break time="250ms"/>')
        parsed = parsed.replace("[lip-smack]", '<break time="150ms"/>')

        # Wrapping tags
        parsed = re.sub(r'<whisper>(.*?)</whisper>', r'<prosody volume="-15%" pitch="-4Hz" rate="-10%">\1</prosody>', parsed)
        parsed = re.sub(r'<soft>(.*?)</soft>', r'<prosody volume="-10%" pitch="-2Hz" rate="-6%">\1</prosody>', parsed)
        parsed = re.sub(r'<slow>(.*?)</slow>', r'<prosody rate="-14%">\1</prosody>', parsed)
        parsed = re.sub(r'<lower-pitch>(.*?)</lower-pitch>', r'<prosody pitch="-4Hz">\1</prosody>', parsed)
        parsed = re.sub(r'<emphasis>(.*?)</emphasis>', r'<emphasis level="strong">\1</emphasis>', parsed)

        return parsed

    def clean_plain_text_for_tts(self, text: str) -> str:
        """Removes speech tags and emojis when rendering to plain TTS engines."""
        clean = re.sub(r'\[.*?\]', '', text)
        clean = re.sub(r'<.*?>', '', clean)
        clean = clean.replace("...", ", ")
        for emoji in ["✨", "💖", "😭", "💅", "💋", "🔥", "👀", "🤫"]:
            clean = clean.replace(emoji, "")
        return clean.strip()

    def apply_sexyvoice_acoustic_mastering(self, input_audio_path: str, output_audio_path: str) -> bool:
        """
        Applies SexyVoice high-end vocal mastering DSP chain via FFmpeg:
        1. Deep chest resonance boost (+4.5dB @ 190Hz) for sultry, rich vocal depth
        2. Intimate warmth & body (+2.0dB @ 400Hz)
        3. Subtle sibilance reduction (-2.0dB @ 8000Hz)
        4. Broadcast proximity compression (threshold: -18dB, ratio: 4.0, attack: 3ms, release: 50ms)
        5. Soft-knee vocal loudness maximization
        """
        import imageio_ffmpeg
        ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [
            ffmpeg_bin, "-y",
            "-i", input_audio_path,
            "-af", (
                "equalizer=f=190:width_type=h:width=100:g=4.5,"
                "equalizer=f=400:width_type=h:width=200:g=1.8,"
                "equalizer=f=3200:width_type=h:width=800:g=1.2,"
                "equalizer=f=8000:width_type=h:width=1500:g=-2.0,"
                "acompressor=threshold=-18dB:ratio=4.0:attack=3:release=50:makeup=3.5,"
                "volume=1.20"
            ),
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            output_audio_path
        ]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)
            return res.returncode == 0 and os.path.exists(output_audio_path) and os.path.getsize(output_audio_path) > 1000
        except Exception as e:
            logger.warning(f"[SEXYVOICE] FFmpeg mastering note: {e}")
            return False

    async def synthesize_seductive_voice(self, text: str, voice_key: str = "ava_seductive", filename_prefix: str = "sexyvoice") -> Tuple[str, float]:
        """
        Synthesizes deep, seductive, intimate voiceover for Maya using SexyVoice.ai architecture.
        """
        voice_info = self.registry.VOICES.get(voice_key, self.registry.VOICES["ava_seductive"])
        voice_name = voice_info["name"]
        raw_mp3 = os.path.join(self.output_dir, f"{filename_prefix}_{int(math.fabs(hash(text)))}.mp3")
        mastered_mp3 = raw_mp3.replace(".mp3", "_seductive_mastered.mp3")

        logger.info(f"[SEXYVOICE] Synthesizing deep seductive voice '{voice_name}' ({voice_info['tone'][:40]}...)")

        # 1. Edge-TTS Seductive Prosody Synthesis
        try:
            import edge_tts
            plain_text = self.clean_plain_text_for_tts(text)
            
            # Format with intimate pauses and sultry pacing
            seductive_text = plain_text
            for marker, repl in [
                ("Spotted:", "Spotted... "),
                ("Listen closely:", "Listen closely... "),
                ("Okay babes,", "Okay babes... "),
                ("Darling,", "Darling... "),
                ("Tell me why", "Tell me why, "),
                ("The wildest part?", "The wildest part... "),
                ("XOXO, Maya", "... XOXO, Maya.")
            ]:
                seductive_text = seductive_text.replace(marker, repl)

            rate = voice_info.get("rate", "-8%")
            pitch = voice_info.get("pitch", "-3Hz")
            volume = voice_info.get("volume", "+15%")

            communicate = edge_tts.Communicate(
                seductive_text,
                voice_name,
                rate=rate,
                pitch=pitch,
                volume=volume
            )
            await communicate.save(raw_mp3)

            # 2. Apply SexyVoice Studio Acoustic Mastering
            if self.apply_sexyvoice_acoustic_mastering(raw_mp3, mastered_mp3):
                final_path = mastered_mp3
            else:
                final_path = raw_mp3

            # Calculate duration
            duration = await self._get_audio_duration(final_path, len(plain_text.split()))
            logger.info(f"[SEXYVOICE] Successfully synthesized seductive voice: {final_path} ({duration:.2f}s)")

            audit_log("SEXYVOICE_SYNTHESIS_SUCCESS", {
                "voice": voice_name,
                "duration": duration,
                "mastered": final_path == mastered_mp3
            })

            return final_path, duration

        except Exception as e:
            logger.error(f"[SEXYVOICE] Synthesis error: {e}")
            raise e

    async def _get_audio_duration(self, audio_path: str, word_count: int = 40) -> float:
        """Retrieves exact audio duration via FFmpeg / ffprobe or accurate word pace."""
        import imageio_ffmpeg
        ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [
            ffmpeg_bin, "-i", audio_path
        ]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
            # Parse Duration: 00:00:15.23
            match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
            if match:
                hours, minutes, seconds = match.groups()
                return float(hours) * 3600 + float(minutes) * 60 + float(seconds)
        except Exception:
            pass
        return max(3.8, word_count / 2.15)

sexyvoice_engine = SexyVoiceEngine()

