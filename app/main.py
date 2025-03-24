"""
main.py – Application entry point for Marginal Tax Calculator API

This module initializes the FastAPI app, registers exception handlers,
and sets up versioned routing for tax calculation endpoints.

@package     marginal_tax_calculator
@framework   FastAPI
@version     1.0.0
@route_base  /api/v1
"""

from fastapi import FastAPI
from app.api.v1 import tax
from app.exceptions.handlers import register_exception_handlers
from app.utils.logger import get_logger
import logging

# ------------------------------------------------------------------------------
# Logging Setup
# ------------------------------------------------------------------------------

# Remove uvicorn default handlers; removed it to use custom logger
uvicorn_loggers = ["uvicorn", "uvicorn.error", "uvicorn.access"]
for name in uvicorn_loggers:
    logging.getLogger(name).handlers.clear()

# Initialize application logger
logger = get_logger(__name__)
logger.info("Starting Marginal Tax Calculator API...")

# ------------------------------------------------------------------------------
# Application Entry Point
# ------------------------------------------------------------------------------

# Initialize FastAPI instance
app = FastAPI(
    title="Marginal Tax Calculator",
    version="1.0.0"
)

# ------------------------------------------------------------------------------
# Exception Handling
# ------------------------------------------------------------------------------

# Register global exception handlers
register_exception_handlers(app)

# ------------------------------------------------------------------------------
# Routing
# ------------------------------------------------------------------------------

# Include versioned tax calculation routes
app.include_router(tax.router, prefix="/api/v1")

logger.info("API setup complete. Ready to handle requests.")