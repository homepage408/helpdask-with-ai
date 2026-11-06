from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import get_logger

logger = get_logger("exceptions")


class AppException(Exception):
    """Base application exception with standardized error details."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        code: str = "INTERNAL_SERVER_ERROR",
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details or []


class NotFoundException(AppException):
    def __init__(
        self,
        message: str = "Resource not found",
        code: str = "RESOURCE_NOT_FOUND",
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            code=code,
            details=details,
        )


class BadRequestException(AppException):
    def __init__(
        self,
        message: str = "Bad request",
        code: str = "BAD_REQUEST",
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            code=code,
            details=details,
        )


class UnauthorizedException(AppException):
    def __init__(
        self,
        message: str = "Authentication required",
        code: str = "UNAUTHORIZED",
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            code=code,
            details=details,
        )


class ForbiddenException(AppException):
    def __init__(
        self,
        message: str = "Access forbidden",
        code: str = "FORBIDDEN",
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            code=code,
            details=details,
        )


class ConflictException(AppException):
    def __init__(
        self,
        message: str = "Resource conflict",
        code: str = "CONFLICT",
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            code=code,
            details=details,
        )


def register_exception_handlers(app: FastAPI) -> None:
    """Register uniform JSON error handlers for all exceptions."""

    @app.exception_handler(AppException)
    async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        formatted_details = [
            {
                "field": ".".join(str(loc) for loc in err["loc"] if loc != "body"),
                "message": err["msg"],
                "type": err["type"],
            }
            for err in exc.errors()
        ]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Validation failed for request input",
                    "details": formatted_details,
                }
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        code_map = {
            404: "RESOURCE_NOT_FOUND",
            401: "UNAUTHORIZED",
            403: "FORBIDDEN",
            405: "METHOD_NOT_ALLOWED",
        }
        code = code_map.get(exc.status_code, "HTTP_ERROR")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": code,
                    "message": str(exc.detail),
                    "details": [],
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled server error: %s", str(exc))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected internal server error occurred",
                    "details": [],
                }
            },
        )
