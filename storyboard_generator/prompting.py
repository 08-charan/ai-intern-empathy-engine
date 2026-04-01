from __future__ import annotations

from shared.keywords import extract_keywords

STYLE_LIBRARY = {
    'cinematic': 'cinematic lighting, dramatic composition, highly detailed, professional storyboard frame',
    'digital art': 'digital art, vibrant colors, polished illustration, storyboard panel',
    'photorealistic': 'photorealistic, natural light, realistic textures, documentary-style shot',
    'minimal': 'minimalist design, clean layout, bold subject, editorial illustration',
}

def build_prompt(scene_text: str, style: str = 'cinematic') -> str:
    keywords = extract_keywords(scene_text, limit=5)
    style_phrase = STYLE_LIBRARY.get(style.lower(), STYLE_LIBRARY['cinematic'])
    key_phrase = ', '.join(keywords) if keywords else 'important scene details'
    return (
        f"A visual scene inspired by: {scene_text}. "
        f"Focus on: {key_phrase}. "
        f"Style: {style_phrase}. "
        f"Include clear subject, environment, mood, and storytelling clarity."
    )
