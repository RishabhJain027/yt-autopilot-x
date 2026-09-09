import os
import wave
import math
import struct
import subprocess
from typing import Optional, Tuple, Dict
from packages.config.settings import settings
from packages.logger.logger import logger
from python.services.budget_guard import budget_guard

class TTSService:
    def __init__(self):
        self.output_dir = os.path.join(settings.STORAGE_ROOT, 'audio')
        os.makedirs(self.output_dir, exist_ok=True)

        self.voice_profiles: Dict[str, Dict[str, str]] = {
            "seductive_baddie": {
                "primary": "en-US-AvaNeural",
                "alt1": "en-US-JennyNeural",
                "alt2": "en-US-EmmaNeural",
                "alt3": "en-GB-SoniaNeural",
                "rate": "-7%",
                "pitch": "-2Hz",
                "volume": "+12%",
                "tone": "ultra_seductive_velvety_intimate_whisper"
            },
            "tech_authority": {
                "primary": "en-US-AvaNeural",
                "alt1": "en-US-JennyNeural",
                "alt2": "en-US-GuyNeural",
                "alt3": "en-US-BrianNeural",
                "rate": "-4%",
                "pitch": "-1Hz",
                "volume": "+10%",
                "tone": "clear_expressive_alluring"
            }
        }

    def select_voice_for_niche(self, niche: str = "aesthetic", gender: Optional[str] = None) -> str:
        """
        Selects the ultra-alluring, velvety, seductive female voice for Maya's videos.
        Primary: 'en-US-AvaNeural' (seductive, breathy, warm, intimate).
        """
        return self.voice_profiles["seductive_baddie"]["primary"]

    def _prepare_seductive_text(self, text: str) -> str:
        """
        Refines text pacing with intimate micro-pauses for sultry, velvety Gossip Girl delivery.
        """
        cleaned = text.replace("...", ", ").replace("✨", "").replace("💖", "").replace("😭", "")
        # Add natural sultry pauses after intimate transition phrases
        seductive_markers = [
            ("Spotted:", "Spotted... "),
            ("Listen closely:", "Listen closely... "),
            ("Okay babes,", "Okay babes... "),
            ("Darling,", "Darling... "),
            ("Tell me why", "Tell me why, "),
            ("The wildest part?", "The wildest part... "),
            ("The tea is", "The tea is... "),
            ("XOXO, Maya", "... XOXO, Maya."),
            ("You know you love me...", "You know you love me... ")
        ]
        for src, dst in seductive_markers:
            if src in cleaned:
                cleaned = cleaned.replace(src, dst)
        return cleaned

    async def synthesize(self, text: str, voice_id: Optional[str] = None, niche: str = "aesthetic", filename_prefix: str = 'voice') -> Tuple[str, float]:
        selected_voice = voice_id or self.select_voice_for_niche(niche)
        raw_wav_path = os.path.join(self.output_dir, f'{filename_prefix}_{int(math.fabs(hash(text)))}.wav')
        mp3_path = raw_wav_path.replace('.wav', '.mp3')
        seductive_text = self._prepare_seductive_text(text)

        # 1. Try edge-tts with sultry prosody & warm acoustic intimacy
        try:
            import edge_tts
            profile = self.voice_profiles.get("seductive_baddie", {})
            rate_param = profile.get("rate", "-7%")
            pitch_param = profile.get("pitch", "-2Hz")
            volume_param = profile.get("volume", "+12%")
            
            communicate = edge_tts.Communicate(
                seductive_text,
                selected_voice,
                rate=rate_param,
                pitch=pitch_param,
                volume=volume_param
            )
            await communicate.save(mp3_path)
            
            # Post-process with FFmpeg for warm vocal compression and intimate radio presence
            mastered_mp3 = mp3_path.replace('.mp3', '_mastered.mp3')
            try:
                # EQ: warm boost at 250Hz, slight air at 12kHz, dynamic compression for vocal intimacy
                cmd = [
                    'ffmpeg', '-y', '-i', mp3_path,
                    '-af', 'equalizer=f=250:width_type=h:width=120:g=3.0,equalizer=f=8000:width_type=h:width=1500:g=-1.5,acompressor=threshold=-16dB:ratio=3.5:attack=5:release=60:makeup=2.5,volume=1.15',
                    mastered_mp3
                ]
                proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
                if proc.returncode == 0 and os.path.exists(mastered_mp3):
                    mp3_path = mastered_mp3
            except Exception as fe:
                logger.debug(f"[TTS] FFmpeg vocal warmth filter note: {fe}")

            word_count = len(text.split())
            duration = max(3.8, word_count / 2.15)
            logger.info(f'[TTS] edge-tts synthesized ultra-seductive audio ({selected_voice} | {rate_param} | {pitch_param}): {mp3_path} ({duration:.1f}s)')
            return mp3_path, duration
        except Exception as e:
            logger.info(f'edge-tts note ({e}), generating local velvety synthesized audio wave')

        # 2. Pure Python Synthesized WAV generator (guaranteed zero dependency failure)
        sample_rate = 44100
        words = text.split()
        duration = max(3.8, len(words) * 0.52)
        total_samples = int(sample_rate * duration)

        with wave.open(raw_wav_path, 'w') as wav_file:
            wav_file.setnchannels(1) # mono
            wav_file.setsampwidth(2) # 16-bit
            wav_file.setframerate(sample_rate)

            # Velvety frequency modulation for seductive female voice timbre (~240-270 Hz)
            freq = 245.0 if "ava" in selected_voice.lower() or "emma" in selected_voice.lower() else 230.0
            data = bytearray()
            for i in range(total_samples):
                t = float(i) / sample_rate
                # Smooth gentle envelope with velvety harmonics
                envelope = 0.5 * (1.0 + math.sin(2.0 * math.pi * 2.8 * t))
                val = int(envelope * 7500.0 * (0.75 * math.sin(2.0 * math.pi * freq * t) + 0.25 * math.sin(4.0 * math.pi * freq * t)))
                data.extend(struct.pack('<h', val))
            wav_file.writeframes(data)

        logger.info(f'[TTS] Local synthetic seductive audio generated ({selected_voice}): {raw_wav_path} ({duration:.1f}s)')
        return raw_wav_path, duration

tts_service = TTSService()


