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
        
        img = Image.new('RGB', size, color='#0F172A')
        draw = ImageDraw.Draw(img)

        # Gradient / Accent background bars
        for i in range(0, size[1], 4):
            r = int(15 + (i / size[1]) * 35)
            g = int(23 + (i / size[1]) * 20)
            b = int(42 + (i / size[1]) * 80)
            draw.line([(0, i), (size[0], i)], fill=(r, g, b))

        # Vibrant glowing accent rectangle
        draw.rectangle([40, 40, size[0] - 40, size[1] - 40], outline='#EC4899', width=6)
        draw.rectangle([60, size[1] - 180, size[0] - 60, size[1] - 60], fill='#E11D48')

        # Text banner
        header_text = title[:40].upper()
        draw.text((80, 100), 'YT-AUTOPILOT-X ORIGINAL', fill='#38BDF8')
        draw.text((80, 180), header_text, fill='#FFFFFF')
        if subtitle:
            draw.text((80, size[1] - 140), subtitle.upper()[:35], fill='#FFFFFF')

        img.save(filepath, format='PNG')
        logger.info(f'[IMAGE] Thumbnail generated: {filepath} ({size[0]}x{size[1]})')
        return filepath

image_service = ImageService()
