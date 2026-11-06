from fastapi import APIRouter

from app.delivery.http.v1.endpoints.health import router as health_router

v1_router = APIRouter()
v1_router.include_router(health_router)
