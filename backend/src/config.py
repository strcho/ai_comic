from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from functools import lru_cache
import os
from pathlib import Path


class Settings(BaseSettings):
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_IMAGE_MODEL: str = "dall-e-3"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    FRONTEND_PORT: int = 5173
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    LOG_LEVEL: str = "INFO"
    MAX_RETRIES: int = 3
    REQUEST_TIMEOUT: int = 120
    IMAGE_SIZE: int = 1024
    IMAGE_QUALITY: str = "standard"
    CACHE_TTL: int = 3600
    DB_PATH: str = "sqlite:///./comics.db"
    OUTPUT_DIR: str = "./output"
    CACHE_DIR: str = "./cache"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def ensure_directories():
    settings = get_settings()
    Path(settings.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.CACHE_DIR).mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)