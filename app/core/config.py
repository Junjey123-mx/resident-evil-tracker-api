from functools import lru_cache
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application metadata
    app_name: str = "Resident Evil Franchise Tracker API"
    app_env: str = "development"
    app_version: str = "0.1.0"

    # PostgreSQL connection — either a full URL or individual components
    database_url: str | None = None
    db_user: str | None = None
    db_password: str | None = None
    db_host: str | None = None
    db_port: int = 5432
    db_name: str | None = None

    # Comma-separated list of allowed CORS origins; parsed in app/core/cors.py
    backend_cors_origins: str = ""

    # Cloudinary cover upload settings
    cloudinary_cloud_name: str | None = None
    cloudinary_api_key: str | None = None
    cloudinary_api_secret: str | None = None
    cloudinary_folder: str = "resident-evil-tracker/covers"

    # extra="ignore" allows .env files with legacy or unrelated variables
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def get_database_url(self) -> str:
        if self.db_user and self.db_password and self.db_host and self.db_name:
            user = quote_plus(self.db_user)
            password = quote_plus(self.db_password)
            return f"postgresql://{user}:{password}@{self.db_host}:{self.db_port}/{self.db_name}"
        if self.database_url:
            return self.database_url
        raise ValueError("No database connection configured. Set DATABASE_URL or DB_USER/DB_PASSWORD/DB_HOST/DB_NAME.")


@lru_cache
def get_settings() -> Settings:
    return Settings()
