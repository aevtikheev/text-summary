"""Environment-specific settings for the application."""
import logging
from functools import lru_cache

from pydantic import BaseSettings, AnyUrl

logger = logging.getLogger('uvicorn')


class Settings(BaseSettings):
    """Environment settings for web application."""
    environment: str = 'dev'
    testing: bool = False
    database_url: AnyUrl


@lru_cache()
def get_settings() -> Settings:
    """Load environment settings."""
    logger.info('Loading environment settings...')
    settings = Settings()
    logger.info(f'{settings.environment=} {settings.testing=}')

    return settings
