from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from app.infrastructure.database.connection import close_db_engine
from app.main import app


@pytest.fixture(autouse=True)
async def cleanup_db_connections() -> AsyncGenerator[None, None]:
    """Ensure database connection pools are cleanly closed per test."""
    yield
    await close_db_engine()


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Provide an asynchronous HTTP client configured for testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
