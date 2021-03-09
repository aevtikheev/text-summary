import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.api import ping
from app.config import get_settings

app = FastAPI()

register_tortoise(
    app=app,
    db_url=get_settings().database_url,
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


def create_application() -> FastAPI:
    application = FastAPI()

    register_tortoise(
        application,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )

    application.include_router(ping.router)

    return application


app = create_application()
