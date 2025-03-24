import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch("app.api.v1.tax.fetch_tax_brackets", return_value=[
    {"min": 0, "max": 50000, "rate": 0.1},
    {"min": 50000, "max": 100000, "rate": 0.2},
    {"min": 100000, "rate": 0.3}
])
def test_valid_tax_api(mock_fetch):
    """
    Test a valid API call with income falling into two tax brackets.
    Asserts the correct total tax and response structure.
    """
    response = client.get("/api/v1/calculate-tax?income=75000&year=2024")
    assert response.status_code == 200
    data = response.json()
    assert data["income"] == 75000
    assert data["year"] == 2024
    assert data["total_tax"] == 10000.0
    assert "breakdown" in data
    assert len(data["breakdown"]) == 2

def test_api_missing_income_param():
    """
    Ensure API returns 422 when the required 'income' query param is missing.
    """
    response = client.get("/api/v1/calculate-tax?year=2024")
    assert response.status_code == 422
    assert "error" in response.json()

def test_api_missing_year_param():
    """
    Ensure API returns 422 when the required 'year' query param is missing.
    """
    response = client.get("/api/v1/calculate-tax?income=50000")
    assert response.status_code == 422
    assert "error" in response.json()

def test_api_zero_income():
    """
    Test API behavior when income is 0 (should fail validation).
    """
    response = client.get("/api/v1/calculate-tax?income=0&year=2024")
    assert response.status_code == 422
    assert "error" in response.json()