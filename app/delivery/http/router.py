from fastapi import APIRouter

from app.core.config import get_settings
from app.delivery.http.v1.endpoints.health import router as root_health_router
from app.delivery.http.v1.router import v1_router

settings = get_settings()

api_router = APIRouter()
# Mount root /health for direct health check probes
api_router.include_router(root_health_router)
# Mount v1 router under /api/v1 prefix
api_router.include_router(v1_router, prefix=settings.API_V1_PREFIX)
