"""
tax.py – API route definitions for the Marginal Tax Calculator

Defines the endpoint for calculating income tax. Routes incoming requests to
the business logic layer and returns a structured tax response.

@route     /api/v1/calculate-tax
@response  TaxResponse (total tax, effective rate, and breakdown)
"""

from fastapi import APIRouter, Query
from app.models.tax import TaxResponse
from app.services.tax_service import fetch_tax_brackets, calculate_tax
from datetime import datetime
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.get("/calculate-tax", response_model=TaxResponse)
def calculate_tax_endpoint(
    income: float = Query(..., gt=0, description="Annual income in CAD (e.g., 85000)"),
    year: int = Query(..., ge=2000, le=datetime.now().year + 1, description="Tax year (e.g., 2024)")
):
    """
    Calculates federal income tax based on annual income and tax year.

    Args:
        income (float): The user's annual income (must be > 0)
        year (int): Tax year between 2000 and next calendar year

    Returns:
        TaxResponse: Contains total tax, effective tax rate, and bracket breakdown
    """
    logger.info(f"Received tax calculation request for income={income}, year={year}")

    try:
        # Fetch tax brackets from external tax service (API)
        brackets = fetch_tax_brackets(year)
        
        logger.debug(f"Fetched tax brackets for year {year}: {brackets}")

        # Perform the actual tax calculation based on marginal rates
        total_tax, breakdown = calculate_tax(income, brackets)
        effective = round(total_tax / income, 4)

        logger.info(f"Calculated tax: total={total_tax}, effective_rate={effective}")

        return {
            "income": income,
            "year": year,
            "total_tax": total_tax,
            "effective_tax_rate": effective,
            "breakdown": breakdown
        }

    except Exception as e:
        logger.error(f"Error calculating tax for income={income}, year={year} - {str(e)}")
        raise