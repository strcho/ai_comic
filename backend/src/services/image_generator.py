from openai import AsyncOpenAI
from typing import List
import httpx
import os
from src.config import get_settings
from src.models import Scene
from src.utils.logger import get_logger

logger = get_logger("image_generator")


class ImageGenerator:
    def __init__(self):
        settings = get_settings()
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_IMAGE_MODEL
        self.size = settings.IMAGE_SIZE
        self.quality = settings.IMAGE_QUALITY
        self.style = "vivid"

    async def generate_images(self, scenes: List[Scene]) -> List[Scene]:
        logger.info(f"Generating images for {len(scenes)} scenes")
        
        for scene in scenes:
            prompt = self._build_prompt(scene)
            try:
                image_url = await self._generate_image(prompt)
                scene.image_prompt = prompt
                scene.image_url = image_url
                logger.info(f"Generated image for scene {scene.id}")
            except Exception as e:
                logger.error(f"Failed to generate image for scene {scene.id}: {e}")
                scene.image_url = None
        
        return scenes

    def _build_prompt(self, scene: Scene) -> str:
        return f"Comic book panel: {scene.cleaned_description}. {self.style} style, high quality, detailed illustration."

    async def _generate_image(self, prompt: str) -> str:
        response = await self.client.images.generate(
            model=self.model,
            prompt=prompt,
            n=1,
            size=f"{self.size}x{self.size}",
            quality=self.quality,
            style=self.style,
        )
        return response.data[0].url

    async def download_images(self, scenes: List[Scene], output_dir: str) -> List[Scene]:
        import aiofiles
        from pathlib import Path
        
        logger.info(f"Downloading {len(scenes)} images to {output_dir}")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            for scene in scenes:
                if scene.image_url:
                    try:
                        response = await client.get(scene.image_url)
                        if response.status_code == 200:
                            filename = f"scene_{scene.id}.png"
                            filepath = os.path.join(output_dir, filename)
                            async with aiofiles.open(filepath, 'wb') as f:
                                await f.write(response.content)
                            scene.image_path = filepath
                            logger.info(f"Downloaded scene {scene.id} to {filepath}")
                    except Exception as e:
                        logger.error(f"Failed to download image for scene {scene.id}: {e}")
        
        return scenes