from __future__ import annotations

import base64
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in ['DejaVuSans.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
        try:
            return ImageFont.truetype(name, size=size)
        except Exception:
            pass
    return ImageFont.load_default()


def generate_local_image(prompt: str, caption: str, output_path: str, style: str = 'cinematic') -> str:
    """Fallback renderer that produces a rich storyboard card locally."""
    w, h = 1024, 768
    img = Image.new('RGB', (w, h), (248, 248, 250))
    draw = ImageDraw.Draw(img)

    for y in range(0, h, 32):
        shade = 236 + (y // 32) % 8
        draw.rectangle([0, y, w, y + 31], fill=(shade, shade, shade + 2))

    draw.rounded_rectangle([30, 30, w - 30, h - 30], radius=24, outline=(60, 60, 60), width=4)

    title_font = _load_font(34)
    body_font = _load_font(24)
    small_font = _load_font(18)

    lines = [
        f'Style: {style}',
        f'Prompt: {prompt[:180]}{"..." if len(prompt) > 180 else ""}',
    ]

    draw.text((60, 60), caption, font=title_font, fill=(20, 20, 20))
    y = 130
    for line in lines:
        draw.multiline_text((60, y), line, font=body_font, fill=(45, 45, 45), spacing=8)
        y += 120

    box_colors = [(90, 125, 180), (180, 120, 90), (110, 170, 120)]
    for i, color in enumerate(box_colors):
        x1 = 80 + i * 280
        y1 = 460
        draw.rounded_rectangle([x1, y1, x1 + 220, y1 + 160], radius=20, fill=color)
        draw.text((x1 + 18, y1 + 18), f'Scene {i + 1}', font=small_font, fill=(255, 255, 255))

    draw.text((60, 650), 'Local storyboard render (API optional)', font=small_font, fill=(80, 80, 80))
    img.save(output_path)
    return output_path


def generate_image(prompt: str, caption: str, output_path: str, style: str = 'cinematic') -> str:
    api_key = os.getenv('OPENAI_API_KEY', '').strip()
    model = os.getenv('OPENAI_IMAGE_MODEL', 'gpt-image-1').strip()

    if api_key and OpenAI is not None:
        try:
            client = OpenAI(api_key=api_key)
            result = client.images.generate(
                model=model,
                prompt=prompt,
                size='1024x1024',
            )
            data = getattr(result, 'data', None) or []
            if data:
                first = data[0]
                if getattr(first, 'b64_json', None):
                    raw = base64.b64decode(first.b64_json)
                    Path(output_path).write_bytes(raw)
                    return output_path
                if getattr(first, 'url', None):
                    import urllib.request
                    urllib.request.urlretrieve(first.url, output_path)
                    return output_path
        except Exception:
            pass

    return generate_local_image(prompt, caption, output_path, style)
