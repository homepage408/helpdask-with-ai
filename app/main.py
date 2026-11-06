from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import get_logger, setup_logging
from app.delivery.http.middleware.request_id import RequestIDMiddleware
from app.delivery.http.router import api_router
from app.infrastructure.database.connection import check_db_connection, close_db_engine

logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for graceful startup and shutdown."""
    # Startup
    setup_logging()
    settings = get_settings()
    logger.info("Starting up %s in [%s] mode...", settings.PROJECT_NAME, settings.ENVIRONMENT)

    db_ready = await check_db_connection()
    if db_ready:
        logger.info("Database connection successfully established.")
    else:
        logger.warning("Database connection could not be established on startup.")

    yield

    # Shutdown
    logger.info("Shutting down %s...", settings.PROJECT_NAME)
    await close_db_engine()
    logger.info("Application shutdown completed.")


def create_application() -> FastAPI:
    """Factory function to build and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # Middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIDMiddleware)

    # Centralized Exception Handlers
    register_exception_handlers(app)

    # Routes
    app.include_router(api_router)

    return app


app = create_application()
