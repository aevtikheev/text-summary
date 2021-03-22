"""Module to work with summarizer database."""
import logging

from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

from app.config import get_settings

TORTOISE_ORM = {
    'connections': {'default': get_settings().database_url},
    'apps': {
        'models': {
            'models': ['app.models', 'aerich.models'],
            'default_connection': 'default',
        },
    },
}

logger = logging.getLogger('uvicorn')


def init_db(app: FastAPI) -> None:
    """Register Tortoise ORM."""
    register_tortoise(
        app=app,
        db_url=get_settings().database_url,
        modules={'models': ['app.models']},
        generate_schemas=False,
        add_exception_handlers=True,
    )


async def generate_schema() -> None:
    """Generate DB schemes for summarizer app."""
    logger.info('Initializing Tortoise...')

    await Tortoise.init(
        db_url=get_settings().database_url,
        modules={'models': ['app.models']},
    )
    logger.info('Generating database schema via Tortoise...')
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == '__main__':
    run_async(generate_schema())
