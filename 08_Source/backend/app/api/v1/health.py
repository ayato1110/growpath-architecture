from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.schemas.auth import Health

router = APIRouter(tags=["health"])

APP_VERSION = "0.1.0"


@router.get("/health", response_model=Health)
def health(settings: Settings = Depends(get_settings)) -> Health:
    return Health(
        status="ok", version=APP_VERSION, dependencies={"auth": settings.auth_mode}
    )
