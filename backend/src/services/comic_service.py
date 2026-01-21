import uuid
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
import os
from src.models import Scene, ComicRequest, ComicResponse
from src.services.story_processor import StoryProcessor
from src.services.image_generator import ImageGenerator
from src.services.comic_composer import ComicComposer
from src.config import get_settings
from src.utils.logger import get_logger

logger = get_logger("comic_service")


class ComicService:
    def __init__(self):
        self.story_processor = StoryProcessor()
        self.image_generator = ImageGenerator()
        self.comic_composer = ComicComposer()
        self.settings = get_settings()
        self.tasks: Dict[str, Dict[str, Any]] = {}

    async def generate_comic(
        self,
        text: str,
        output_format: str = "png",
        output_path: str = None
    ) -> Dict[str, Any]:
        task_id = str(uuid.uuid4())
        logger.info(f"Starting comic generation task {task_id}")
        
        try:
            self.tasks[task_id] = {
                "id": task_id,
                "status": "processing",
                "created_at": datetime.now().isoformat(),
                "progress": 0
            }
            
            scenes = self.story_processor.parse_story(text)
            self._update_task_progress(task_id, 20)
            
            scenes = await self.image_generator.generate_images(scenes)
            self._update_task_progress(task_id, 60)
            
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"comic_{timestamp}.{output_format}"
                output_path = os.path.join(self.settings.OUTPUT_DIR, filename)
            
            temp_dir = os.path.join(self.settings.CACHE_DIR, task_id)
            scenes = await self.image_generator.download_images(scenes, temp_dir)
            self._update_task_progress(task_id, 80)
            
            final_output = self.comic_composer.compose_comic(
                scenes, output_path, output_format
            )
            self._update_task_progress(task_id, 100)
            
            self.tasks[task_id].update({
                "status": "completed",
                "output_path": final_output,
                "scenes": [s.dict() for s in scenes]
            })
            
            logger.info(f"Comic generation task {task_id} completed successfully")
            return self.tasks[task_id]
            
        except Exception as e:
            logger.error(f"Comic generation task {task_id} failed: {e}")
            self.tasks[task_id].update({
                "status": "failed",
                "error": str(e)
            })
            raise

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        return self.tasks[task_id]

    def get_history(self) -> List[Dict[str, Any]]:
        completed_tasks = [
            task for task in self.tasks.values()
            if task.get("status") == "completed"
        ]
        return sorted(
            completed_tasks,
            key=lambda x: x.get("created_at", ""),
            reverse=True
        )[:10]

    def _update_task_progress(self, task_id: str, progress: int):
        if task_id in self.tasks:
            self.tasks[task_id]["progress"] = progress
            logger.debug(f"Task {task_id} progress: {progress}%")