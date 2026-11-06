import pytest
from httpx import AsyncClient

from app.core.exceptions import AppException, NotFoundException


def test_app_exception_hierarchy() -> None:
    """Ensure custom exceptions have expected status codes and default error envelopes."""
    exc = NotFoundException("Ticket not found")
    assert isinstance(exc, AppException)
    assert exc.status_code == 404
    assert exc.code == "RESOURCE_NOT_FOUND"
    assert exc.message == "Ticket not found"


@pytest.mark.asyncio
async def test_404_error_envelope(async_client: AsyncClient) -> None:
    """Ensure standard 404 returns structured error JSON."""
    response = await async_client.get("/non-existent-endpoint-path")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "RESOURCE_NOT_FOUND"
