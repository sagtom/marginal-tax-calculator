import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from app.services.tax_service import fetch_tax_brackets, calculate_tax
from app.core.config import settings
from requests.exceptions import RequestException


def test_tax_calculation_basic():
    """
    Test tax calculation for income spanning multiple brackets.
    Confirms correct tax and breakdown structure.
    """
    brackets = [
        {"min": 0, "max": 50000, "rate": 0.1},
        {"min": 50000, "max": 100000, "rate": 0.2}
    ]
    tax, breakdown = calculate_tax(75000, brackets)
    assert tax == 10000.0
    assert len(breakdown) == 2


def test_tax_calculation_top_bracket():
    """
    Test income exceeding the last defined bracket max.
    Ensures the top bracket without 'max' is handled.
    """
    brackets = [
        {"min": 0, "max": 50000, "rate": 0.1},
        {"min": 50000, "max": 100000, "rate": 0.2},
        {"min": 100000, "rate": 0.3}
    ]
    tax, breakdown = calculate_tax(150000, brackets)
    assert tax == 30000.0
    assert breakdown[-1]["taxable_income"] == 50000


def test_tax_calculation_income_below_threshold():
    """
    Test when income is below the first bracket's minimum threshold.
    Should return 0 tax and empty breakdown.
    """
    brackets = [{"min": 10000, "max": 20000, "rate": 0.1}]
    tax, breakdown = calculate_tax(9000, brackets)
    assert tax == 0.0
    assert breakdown == []


@patch("app.services.tax_service.requests.get")
def test_fetch_tax_brackets_success(mock_get):
    """
    Test successful fetch of tax brackets from external API.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "tax_brackets": [{"min": 0, "max": 50000, "rate": 0.1}]
    }

    brackets = fetch_tax_brackets(2024)
    assert isinstance(brackets, list)
    assert brackets[0]["rate"] == 0.1


@patch("app.services.tax_service.requests.get")
def test_fetch_tax_brackets_failure_without_retry(mock_get):
    """
    Test API fetch failure when retries are disabled.
    Should raise HTTPException after one failed attempt.
    """
    settings.api_retry_enabled = False
    mock_get.side_effect = RequestException("API failure")

    with pytest.raises(HTTPException) as exc:
        fetch_tax_brackets(2024)
    assert exc.value.status_code == 500

@patch("app.services.tax_service.requests.get")
def test_fetch_tax_brackets_retry_success(mock_get):
    """
    Test successful API response after initial failure with retries enabled.
    """
    settings.api_retry_enabled = True
    settings.api_max_retries = 3

    mock_get.side_effect = [
        RequestException("fail"),
        RequestException("fail"),
        MagicMock(status_code=200, json=lambda: {"tax_brackets": [{"min": 0, "rate": 0.1}]})
    ]

    brackets = fetch_tax_brackets(2024)
    assert len(brackets) == 1
    assert brackets[0]["rate"] == 0.1


@patch("app.services.tax_service.requests.get")
def test_fetch_tax_brackets_all_attempts_fail(mock_get):
    """
    Test all retry attempts fail, and it raises HTTPException.
    """
    settings.api_retry_enabled = True
    settings.api_max_retries = 2
    mock_get.side_effect = RequestException("API still down")

    with pytest.raises(HTTPException) as exc:
        fetch_tax_brackets(2024)

    assert exc.value.status_code == 500
    assert exc.value.detail == "Could not fetch tax data"