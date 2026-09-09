import os
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, List, Optional
from packages.config.settings import settings
from packages.logger.logger import logger

class ImageService:
    def __init__(self):
        self.output_dir = os.path.join(settings.STORAGE_ROOT, 'thumbnails')
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_thumbnail(self, title: str, subtitle: str = '', aspect_ratio: str = '16:9', filename_prefix: str = 'thumb') -> str:
        if aspect_ratio == '9:16':
            size = (1080, 1920)
        else:
            size = (1280, 720)

        filepath = os.path.join(self.output_dir, f'{filename_prefix}_{os.getpid()}_{int(abs(hash(title)))}.png')
        
        img = Image.new('RGB', size, color='#180F1E')
        draw = ImageDraw.Draw(img)

        # Dreamy Gossip Girl Rose Gold, Amber & Obsidian Manhattan Gradient
        for i in range(0, size[1], 4):
            ratio = i / size[1]
            r = int(22 + ratio * 65)
            g = int(14 + ratio * 28)
            b = int(28 + ratio * 32)
            draw.line([(0, i), (size[0], i)], fill=(r, g, b))

        # Vibrant glowing aesthetic border in champagne gold & rose
        draw.rectangle([35, 35, size[0] - 35, size[1] - 35], outline='#D4AF37', width=6)
        draw.rectangle([45, 45, size[0] - 45, size[1] - 45], outline='#EC4899', width=2)
        draw.rectangle([60, size[1] - 220, size[0] - 60, size[1] - 60], fill='#1E1028', outline='#D4AF37', width=2)

        # Text banner for Maya ✨ Gossip Girl
        header_text = title[:45].upper()
        draw.text((80, 90), 'SPOTTED: MAYA ✨ GOSSIP GIRL', fill='#D4AF37')
        draw.text((80, 130), 'UPPER EAST SIDE SECRETS', fill='#F472B6')
        draw.text((80, 190), header_text, fill='#FFFFFF')
        if subtitle:
            draw.text((80, size[1] - 180), subtitle.upper()[:35], fill='#FDF2F8')
        draw.text((80, size[1] - 120), 'YOU KNOW YOU LOVE ME • XOXO MAYA ✨', fill='#F472B6')

        img.save(filepath, format='PNG')
        logger.info(f'[IMAGE] Maya Gossip Girl aesthetic thumbnail generated: {filepath} ({size[0]}x{size[1]})')
        return filepath

image_service = ImageService()
