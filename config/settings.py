import logging
import os
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv(dotenv_path="./.env")


def setup_logging():
    """Configure basic logging for the application."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


class LLMSettings(BaseModel):
    """Base settings for Language Model configurations."""

    temperature: float = 0.5
    max_tokens: Optional[int] = 1024
    top_p: float = 0.65 
    stream: bool = True 
    stop: Optional[str] = None


class LlamaSettings(LLMSettings):
    """llama-specific settings extending LLMSettings."""

    api_key: str = Field(default_factory=lambda: os.getenv("GROQ_API_KEY"))
    default_model: str = Field(default="llama-3.3-70b-versatile")

class Settings(BaseModel):
    """Main settings class combining all sub-settings."""

    LLAMA: LlamaSettings = Field(default_factory=LlamaSettings)

@lru_cache()
def get_settings() -> Settings:
    """Create and return a cached instance of the Settings."""
    settings = Settings()
    setup_logging()
    return settings