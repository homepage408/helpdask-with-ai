import uuid
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

HEADER_REQUEST_ID = "X-Request-ID"


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware that injects a unique X-Request-ID into request and response headers."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = request.headers.get(HEADER_REQUEST_ID) or str(uuid.uuid4())
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers[HEADER_REQUEST_ID] = request_id
        return response
