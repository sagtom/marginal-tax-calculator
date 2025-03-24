"""
config.py – Application configuration using Pydantic Settings

Loads environment variables from a .env file and exposes them
as strongly-typed Python attributes.

@dependency   pydantic-settings
@env_file     .env
"""

from pydantic_settings import BaseSettings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class Settings(BaseSettings):
    tax_api_base: str
    app_port: int = 8000
    log_level: str = "INFO"  # Default log level
    api_retry_enabled: bool = True
    api_max_retries: int = 3

    class Config:
        env_file = ".env"

# Initialize settings and log the current configuration (excluding sensitive)
try:
    settings = Settings()
    logger.info(f"Configuration loaded: tax_api_base={settings.tax_api_base}, app_port={settings.app_port}, log_level={settings.log_level}")
except Exception as e:
    logger.error(f"Failed to load configuration: {e}")
    raise