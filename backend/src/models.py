from pydantic import BaseModel
from typing import List, Optional


class Scene(BaseModel):
    id: int
    description: str
    cleaned_description: str
    image_prompt: Optional[str] = None
    image_url: Optional[str] = None
    image_path: Optional[str] = None


class ComicRequest(BaseModel):
    text: str
    style: Optional[str] = "vivid"
    image_size: Optional[int] = 1024
    format: Optional[str] = "png"
    quality: Optional[str] = "standard"


class ComicResponse(BaseModel):
    id: str
    status: str
    scenes: List[Scene]
    output_path: Optional[str] = None
    error: Optional[str] = None
    created_at: str