from fastapi import APIRouter, Depends

from app.config import get_settings, Settings


router = APIRouter()


@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "11",
        "environment": settings.environment,
        "testing": settings.testing
    }
