"""Main module for summarizer web app."""
import logging

from fastapi import FastAPI

from app.api import summaries
from app.db import init_db


logger = logging.getLogger('uvicorn')


def create_application() -> FastAPI:
    """Create summarizer web application and register it's URLs."""
    application = FastAPI()
    application.include_router(summaries.router, prefix='/summaries', tags=['summaries'])

    return application


app = create_application()


@app.on_event('startup')
async def startup_event() -> None:
    """Initialize ORM for summarizer web app."""
    logger.info('Starting up...')
    init_db(app)
