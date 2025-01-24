from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Configuration de base
    API_KEY: str = "netra0000netra"
    API_KEY_NAME: str = "X-API-Key"
    ALLOW_ORIGINS: str = "http://localhost:5173"  # Une seule URL par défaut
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

    # Base de données
    MONGODB_URL: str = "mongodb://localhost:27017/docprocessing"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "documents"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env"
    )

    def get_cors_origins(self) -> List[str]:
        """Convertit la chaîne ALLOW_ORIGINS en liste"""
        if self.ALLOW_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.ALLOW_ORIGINS.split(",")]

@lru_cache
def get_settings() -> Settings:
    return Settings()

#
# from pydantic_settings import BaseSettings
#
# class Settings(BaseSettings):
#     API_KEY: str = "netra0000netra"
#
# def get_settings():
#     return Settings()