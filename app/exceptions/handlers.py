"""
handlers.py – Global exception handling for the app

This module registers centralized exception handlers for:
- HTTP exceptions (e.g. 404, 400)
- Validation errors from request bodies or query params
- Uncaught exceptions (500 errors)

@used_in main.py
"""

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.logger import get_logger

# Set up a structured application logger
logger = get_logger(__name__)

def register_exception_handlers(app):
    """
    Register global exception handlers for the app.

    Args:
        app (FastAPI): The main application instance.
    """

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """
        Handles HTTP exceptions (e.g., 404 Not Found, 403 Forbidden).

        Returns:
            JSONResponse with the error message and original status code
        """
        logger.warning(f"[HTTPException] {request.method} {request.url} - {exc.status_code}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        Handles validation errors (query params, body parsing, etc.)

        Returns:
            422 Unprocessable Entity response with validation details
        """
        logger.error(f"[ValidationError] {request.method} {request.url} - {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation failed.",
                "details": exc.errors()
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """
        Catches any unhandled exceptions to prevent app crashes.

        Returns:
            500 Internal Server Error with a generic message
        """
        logger.exception(f"[UnhandledException] {request.method} {request.url} - {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error."}
        )