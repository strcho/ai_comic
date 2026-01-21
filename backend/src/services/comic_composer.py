from typing import List
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os
from src.models import Scene
from src.utils.logger import get_logger
import json

logger = get_logger("comic_composer")


class ComicComposer:
    def __init__(self):
        self.panel_size = (1024, 1024)
        self.padding = 20
        self.border_width = 4
        self.background_color = (255, 255, 255)
        self.border_color = (50, 50, 50)

    def compose_comic(
        self, 
        scenes: List[Scene], 
        output_path: str, 
        output_format: str = "png"
    ) -> str:
        logger.info(f"Composing comic with {len(scenes)} scenes, format: {output_format}")
        
        if not scenes or all(not s.image_path for s in scenes):
            raise ValueError("No valid images to compose")
        
        layout = self._calculate_layout(len(scenes))
        composite = self._create_composite_image(scenes, layout)
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        if output_format.lower() == "pdf":
            self._save_pdf(composite, scenes, output_path)
        else:
            composite.save(output_path, format="PNG", quality=95)
        
        self._save_metadata(scenes, output_path)
        logger.info(f"Comic saved to {output_path}")
        return output_path

    def _calculate_layout(self, num_scenes: int):
        if num_scenes == 2:
            return {"rows": 1, "cols": 2}
        elif num_scenes == 3:
            return {"rows": 1, "cols": 3}
        elif num_scenes == 4:
            return {"rows": 2, "cols": 2}
        else:
            return {"rows": 2, "cols": 3}

    def _create_composite_image(self, scenes: List[Scene], layout: dict) -> Image.Image:
        rows = layout["rows"]
        cols = layout["cols"]
        
        total_width = cols * self.panel_size[0] + (cols + 1) * self.padding
        total_height = rows * self.panel_size[1] + (rows + 1) * self.padding
        
        composite = Image.new('RGB', (total_width, total_height), self.background_color)
        draw = ImageDraw.Draw(composite)
        
        for idx, scene in enumerate(scenes):
            if not scene.image_path or not os.path.exists(scene.image_path):
                continue
                
            row = idx // cols
            col = idx % cols
            
            x = self.padding + col * (self.panel_size[0] + self.padding)
            y = self.padding + row * (self.panel_size[1] + self.padding)
            
            try:
                panel = Image.open(scene.image_path)
                panel = panel.resize(self.panel_size, Image.Resampling.LANCZOS)
                composite.paste(panel, (x, y))
                
                x1 = x - self.border_width // 2
                y1 = y - self.border_width // 2
                x2 = x + self.panel_size[0] + self.border_width // 2
                y2 = y + self.panel_size[1] + self.border_width // 2
                
                draw.rectangle([(x1, y1), (x2, y2)], 
                             outline=self.border_color, 
                             width=self.border_width)
                
                logger.debug(f"Placed scene {scene.id} at ({x}, {y})")
            except Exception as e:
                logger.error(f"Failed to place scene {scene.id}: {e}")
        
        return composite

    def _save_pdf(self, image: Image.Image, scenes: List[Scene], output_path: str):
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        
        pdf_path = output_path if output_path.endswith('.pdf') else output_path.replace('.png', '.pdf')
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        for idx, scene in enumerate(scenes):
            if scene.image_path and os.path.exists(scene.image_path):
                img = RLImage(scene.image_path, width=400, height=400)
                story.append(img)
                
                if scene.description:
                    caption = Paragraph(scene.description, styles['BodyText'])
                    story.append(caption)
        
        doc.build(story)
        logger.info(f"PDF saved to {pdf_path}")

    def _save_metadata(self, scenes: List[Scene], output_path: str):
        metadata = {
            "num_scenes": len(scenes),
            "panel_size": self.panel_size,
            "layout": self._calculate_layout(len(scenes)),
            "scenes": [
                {
                    "id": scene.id,
                    "description": scene.description,
                    "image_path": scene.image_path
                }
                for scene in scenes
            ]
        }
        
        metadata_path = output_path.replace('.png', '_metadata.json').replace('.pdf', '_metadata.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        logger.info(f"Metadata saved to {metadata_path}")