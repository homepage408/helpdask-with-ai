from fastapi import APIRouter, Response, status
from pydantic import BaseModel

from app.core.config import get_settings
from app.infrastructure.database.connection import check_db_connection

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    status: str
    database: str
    environment: str
    version: str


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check probe",
    description="Check liveness and readiness of the API and its database connection.",
)
async def health_check(response: Response) -> HealthResponse:
    settings = get_settings()
    db_connected = await check_db_connection()

    db_status = "connected" if db_connected else "disconnected"
    overall_status = "healthy" if db_connected else "degraded"

    if not db_connected:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return HealthResponse(
        status=overall_status,
        database=db_status,
        environment=settings.ENVIRONMENT,
        version="0.1.0",
    )
