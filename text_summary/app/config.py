"""Environment-specific settings for the application."""
from functools import lru_cache
import logging
import os

from pydantic import BaseSettings, AnyUrl

logger = logging.getLogger('uvicorn')


class Settings(BaseSettings):
    environment: str = os.getenv('ENVIRONMENT', 'dev')
    testing: bool = os.getenv('TESTING', False)
    database_url: AnyUrl = os.getenv('DATABASE_URL')


@lru_cache()
def get_settings() -> Settings:
    logger.info('Loading environment settings...')
    return Settings()
