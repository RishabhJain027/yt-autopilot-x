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

        # Dreamy Pinterest Aesthetic Rose Gold & Amber Gradient
        for i in range(0, size[1], 4):
            ratio = i / size[1]
            r = int(24 + ratio * 60)
            g = int(15 + ratio * 20)
            b = int(30 + ratio * 35)
            draw.line([(0, i), (size[0], i)], fill=(r, g, b))

        # Vibrant glowing aesthetic border
        draw.rectangle([40, 40, size[0] - 40, size[1] - 40], outline='#EC4899', width=6)
        draw.rectangle([60, size[1] - 180, size[0] - 60, size[1] - 60], fill='#BE185D')

        # Text banner for Maya ✨ Cutie Baddie
        header_text = title[:42].upper()
        draw.text((80, 100), 'MAYA ✨ BADDIE SECRETS', fill='#F472B6')
        draw.text((80, 180), header_text, fill='#FFFFFF')
        if subtitle:
            draw.text((80, size[1] - 140), subtitle.upper()[:35], fill='#FDF2F8')

        img.save(filepath, format='PNG')
        logger.info(f'[IMAGE] Maya aesthetic thumbnail generated: {filepath} ({size[0]}x{size[1]})')
        return filepath

image_service = ImageService()
