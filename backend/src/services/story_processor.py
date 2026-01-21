from typing import List
from src.models import Scene
from src.utils.logger import get_logger

logger = get_logger("story_processor")


class StoryProcessor:
    def __init__(self):
        self.scene_delimiters = ["\n\n", "\nScene:", "\nPanel:", "\nFrame:"]

    def parse_story(self, text: str) -> List[Scene]:
        logger.info(f"Parsing story text (length: {len(text)})")
        raw_scenes = self._extract_scenes(text)
        cleaned_scenes = self._clean_and_validate(raw_scenes)
        logger.info(f"Extracted {len(cleaned_scenes)} scenes")
        return cleaned_scenes

    def _extract_scenes(self, text: str) -> List[str]:
        scenes = []
        delimiter_used = None

        for delimiter in self.scene_delimiters:
            if delimiter in text:
                delimiter_used = delimiter
                break

        if delimiter_used:
            scenes = [s.strip() for s in text.split(delimiter_used) if s.strip()]
        else:
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            scenes_per_sentence = max(2, min(5, len(sentences) // 2))
            scene_size = max(1, len(sentences) // scenes_per_sentence)
            for i in range(0, len(sentences), scene_size):
                scene_text = '. '.join(sentences[i:i + scene_size])
                if scene_text:
                    scenes.append(scene_text)

        return scenes

    def _clean_and_validate(self, raw_scenes: List[str]) -> List[Scene]:
        cleaned_scenes = []
        
        for idx, scene_text in enumerate(raw_scenes):
            cleaned_text = self._clean_text(scene_text)
            
            if cleaned_text and len(cleaned_text) > 10:
                scene = Scene(
                    id=idx + 1,
                    description=scene_text,
                    cleaned_description=cleaned_text
                )
                cleaned_scenes.append(scene)

        if len(cleaned_scenes) < 2:
            if cleaned_scenes:
                remaining = raw_scenes[len(cleaned_scenes):]
                for scene_text in remaining:
                    cleaned_text = self._clean_text(scene_text)
                    if cleaned_text and len(cleaned_text) > 10:
                        scene = Scene(
                            id=len(cleaned_scenes) + 1,
                            description=scene_text,
                            cleaned_description=cleaned_text
                        )
                        cleaned_scenes.append(scene)
                        if len(cleaned_scenes) >= 2:
                            break

        if len(cleaned_scenes) > 5:
            cleaned_scenes = cleaned_scenes[:5]

        return cleaned_scenes

    def _clean_text(self, text: str) -> str:
        text = ' '.join(text.split())
        text = text.strip()
        if not text.endswith(('.', '!', '?')):
            text = text + '.'
        return text