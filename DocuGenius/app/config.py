"""Application configuration using Pydantic settings"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "DocuGenius"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mistral"
    
    # Meilisearch
    MEILISEARCH_URL: str = "http://localhost:7700"
    MEILISEARCH_MASTER_KEY: str = ""
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".xlsx", ".txt", ".png", ".jpg", ".jpeg"]
    UPLOAD_DIR: str = "uploads"
    
    # Tesseract
    TESSERACT_CMD: str = "tesseract"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

