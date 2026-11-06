import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_endpoint(async_client: AsyncClient) -> None:
    """Ensure root /health endpoint returns healthy status and DB connection."""
    response = await async_client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "version" in data
    assert "environment" in data


@pytest.mark.asyncio
async def test_health_check_v1_endpoint(async_client: AsyncClient) -> None:
    """Ensure /api/v1/health endpoint functions identically."""
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"


@pytest.mark.asyncio
async def test_request_id_middleware(async_client: AsyncClient) -> None:
    """Ensure request ID middleware injects X-Request-ID header."""
    response = await async_client.get("/health")
    assert "x-request-id" in response.headers
    assert len(response.headers["x-request-id"]) > 0
