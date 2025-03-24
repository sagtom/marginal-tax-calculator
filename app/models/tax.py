"""
tax.py – Pydantic data models for tax calculation

Defines the structure for tax brackets, detailed tax breakdowns,
and the response schema returned by the `/calculate-tax` endpoint.

@models
@used_in  api/v1/tax.py, services/tax_service.py
"""

from typing import Optional, List
from pydantic import BaseModel

class TaxBracket(BaseModel):
    # Represents a single tax bracket range from the external API.
    min: float
    max: Optional[float]
    rate: float

class TaxBreakdown(BaseModel):
    # Represents how much tax was applied in a specific bracket.
    min: float
    max: Optional[float]
    rate: float
    taxable_income: float
    tax: float

class TaxResponse(BaseModel):
    # Represents the full response for a tax calculation request.
    income: float
    year: int
    total_tax: float
    effective_tax_rate: float
    breakdown: List[TaxBreakdown]