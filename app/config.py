"""
Application configuration using pydantic-settings.

This validates all environment variables at startup, preventing
runtime errors from missing or invalid configuration.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings are validated at startup. If any required
    setting is missing or invalid, the app won't start.
    """
    
    # Application
    APP_NAME: str = "Hanif Backend API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Using lru_cache ensures we only load and validate
    settings once, then reuse the same instance.
    """
    return Settings()
