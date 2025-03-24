"""
tax_service.py – Business logic for marginal tax calculations.

This module contains:
1. Function to fetch tax brackets from an external API.
2. Function to calculate total income tax using marginal tax rates.
"""

from typing import List, Tuple
from app.core.config import settings
from fastapi import HTTPException
from app.utils.logger import get_logger
import requests
import time

logger = get_logger(__name__)

def fetch_tax_brackets(year: int) -> List[dict]:
    """
    Fetches tax brackets for the given year from the external API.
    Supports optional retries on failure based on configuration.

    Args:
        year (int): Tax year (e.g., 2024)

    Returns:
        List[dict]: A list of tax brackets, each with min, max, and rate keys

    Raises:
        HTTPException: If the external API call fails after retries
    """
    url = f"{settings.tax_api_base}/{year}"
    attempt = 0
    max_attempts = settings.api_max_retries if settings.api_retry_enabled else 1

    while attempt < max_attempts:
        try:
            logger.debug(f"Attempt {attempt + 1} - Fetching tax brackets from: {url}")

            response = requests.get(url)
            response.raise_for_status()
            brackets = response.json().get("tax_brackets", [])

            logger.debug(f"Tax brackets received: {brackets}")

            return brackets
        except requests.RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed to fetch tax brackets: {e}")

            attempt += 1

            if attempt < max_attempts:
                time.sleep(1)
            else:
                logger.error(f"All {max_attempts} attempt(s) failed.")

                raise HTTPException(status_code=500, detail="Could not fetch tax data")

def calculate_tax(income: float, brackets: List[dict]) -> Tuple[float, List[dict]]:
    """
    Calculates total federal tax using marginal tax brackets.

    Args:
        income (float): Annual taxable income
        brackets (List[dict]): List of tax brackets with min, max, and rate

    Returns:
        Tuple[float, List[dict]]: Total tax and detailed breakdown
    """
    logger.info(f"Calculating tax for income: {income}")
    total_tax = 0.0
    breakdown = []

    for bracket in brackets:
        min_income = bracket["min"]
        max_income = bracket.get("max", income)
        rate = bracket["rate"]

        if income <= min_income:
            break

        taxable_income = min(income, max_income) - min_income
        if taxable_income <= 0:
            continue

        tax = taxable_income * rate
        total_tax += tax

        logger.debug(f"Bracket {min_income}-{max_income}: rate={rate}, taxable={taxable_income}, tax={tax}")

        breakdown.append({
            "min": min_income,
            "max": bracket.get("max"),
            "rate": rate,
            "taxable_income": taxable_income,
            "tax": round(tax, 2)
        })

    total_tax = round(total_tax, 2)

    logger.info(f"Total tax calculated: {total_tax}")
    
    return total_tax, breakdown