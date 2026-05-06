from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application metadata
    app_name: str = "Resident Evil Franchise Tracker API"
    app_env: str = "development"
    app_version: str = "0.1.0"

    # PostgreSQL connection string — required, no default
    database_url: str

    # Comma-separated list of allowed CORS origins; parsed in app/core/cors.py
    backend_cors_origins: str = ""

    # Cloudinary cover upload settings
    cloudinary_cloud_name: str | None = None
    cloudinary_api_key: str | None = None
    cloudinary_api_secret: str | None = None
    cloudinary_folder: str = "resident-evil-tracker/covers"

    # extra="ignore" allows .env files with legacy or unrelated variables
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
