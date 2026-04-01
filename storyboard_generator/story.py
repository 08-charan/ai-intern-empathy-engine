from __future__ import annotations

from dataclasses import dataclass
from typing import List

from shared.text_utils import split_into_three_scenes
from storyboard_generator.prompting import build_prompt

@dataclass
class StoryScene:
    caption: str
    prompt: str


def build_story_scenes(text: str, style: str = 'cinematic') -> List[StoryScene]:
    scenes = split_into_three_scenes(text)
    if not scenes:
        return []
    return [StoryScene(caption=s, prompt=build_prompt(s, style=style)) for s in scenes]
