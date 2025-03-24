# Marginal Tax Calculator API

A **FastAPI** service for calculating Canadian federal income tax based on user-provided income and tax year. The API fetches up-to-date tax brackets, computes marginal income tax, and returns structured output for integration in any systems.

---

## Project Structure

```
marginal_tax_calculator/
│
├── app/
│   ├── api/v1/tax.py                 # API route definitions
│   ├── core/config.py                # App settings and environment loading
│   ├── exceptions/handlers.py        # Global exception handlers
│   ├── main.py                       # FastAPI application instance
│   ├── models/tax.py                 # Pydantic models and response schemas
│   ├── services/tax_service.py       # Business logic
│   ├── utils/logger.py               # Custom logger configuration
│
├── tests/
│   └── api/test_tax.py               # Unit tests for API logic
│   └── services/test_tax_service.py  # Unit tests for Service logic
├── .env                              # Environment-specific variables
├── requirements.txt                  # Python package dependencies
├── setup.py                          # Python project setup file
└── README.md
```
---

## System Flow: Marginal Tax Calculator API

This diagram illustrates the high-level request flow and components involved in the Marginal Tax Calculator API architecture.

[![](https://mermaid.ink/img/pako:eNptkk1PwzAMhv-KlTOFew9I-ygbEx8TKxxIETKpt1WkSZWksAn477jpWEEip8R-_Mavkw-hbEkiFWtt39UWXYB8WhjgNZITXZEJKYydfffkwDpYWh9qNE-QJOefsyyHM4VatRoDJQF3nzCWF-jDaHkJo6aBBGqszGmzf-o1x10dTGSXv7NtYNEEuG4gJpGYygfUVYmhsgaucB-55b5EEyp1IKeRzOSK3Ful6Iix3LPvY4NsFuELme34ToMaug4iCy8O1SsF_4ecyZxTk4O32IXdHK-eRWYu78g31niCax6iZj0u-okd0HlEL-VidXsDRz5Y6IfL1OAGBtOZczztrnTBPStqYg9zNKWOJrf9zv91CPM8Xw54LP-VvTe0a0gFKuFfaNH3WhhxImpy_HQl_4yPLlmIsKWaCpHytqQ1tjoUojBfjGIb7GpvlEiDa-lEONtutiJdo_Z8aht2RNMKNw7rY7RB82jtz_nrG2spzW4?type=png)](https://mermaid.live/edit#pako:eNptkk1PwzAMhv-KlTOFew9I-ygbEx8TKxxIETKpt1WkSZWksAn477jpWEEip8R-_Mavkw-hbEkiFWtt39UWXYB8WhjgNZITXZEJKYydfffkwDpYWh9qNE-QJOefsyyHM4VatRoDJQF3nzCWF-jDaHkJo6aBBGqszGmzf-o1x10dTGSXv7NtYNEEuG4gJpGYygfUVYmhsgaucB-55b5EEyp1IKeRzOSK3Ful6Iix3LPvY4NsFuELme34ToMaug4iCy8O1SsF_4ecyZxTk4O32IXdHK-eRWYu78g31niCax6iZj0u-okd0HlEL-VidXsDRz5Y6IfL1OAGBtOZczztrnTBPStqYg9zNKWOJrf9zv91CPM8Xw54LP-VvTe0a0gFKuFfaNH3WhhxImpy_HQl_4yPLlmIsKWaCpHytqQ1tjoUojBfjGIb7GpvlEiDa-lEONtutiJdo_Z8aht2RNMKNw7rY7RB82jtz_nrG2spzW4)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/income-tax-api.git
cd marginal-tax-calculator
```
### Optional - Docker Support

```bash
# Build the Docker image
docker build -t marginal-tax-calculator-api .

# Run it
docker run -p 8000:8000 --env-file .env marginal-tax-calculator-api
```

---
### 2. Install Dependencies

Can create virtual envirnoment if needed for this project by running

```bash
python -m venv venv
source venv/bin/activate
```
then, install requirements

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file using `.env_example` file and passing the required values. (NOte: Adding acutal values expected here for quick setup, in real world application these values won't be exposed in a doc)

```
TAX_API_BASE=http://localhost:5001/tax-calculator/tax-year
*(For Docker Use this)TAX_API_BASE=http://host.docker.internal:5001/tax-calculator/tax-year
APP_PORT=8000
LOG_LEVEL=DEBUG
API_RETRY_ENABLED=true
API_MAX_RETRIES=3
```

### 4. Run the Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Access Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## API Endpoint

### `GET /api/v1/calculate-tax`

NOTE: The API do not respond to tax years above 2023. Expect error for that case. Can be defaulted to last available year but skipped that part.

#### Query Parameters

| Name   | Type  | Required | Description           |
|--------|-------|----------|-----------------------|
| income | float | Yes      | Annual income in CAD  |
| year   | int   | Yes      | Tax year (e.g., 2022) |

#### Example Request

```
GET /api/v1/calculate-tax?income=85000&year=2022
```

#### Example Response

```json
{
  "income": 85000,
  "year": 2022,
  "total_tax": 14167.11,
  "effective_tax_rate": 0.1667,
  "breakdown": [
    {
      "min": 0,
      "max": 50197,
      "rate": 0.15,
      "taxable_income": 50197,
      "tax": 7529.55
    },
    {
      "min": 50197,
      "max": 100392,
      "rate": 0.205,
      "taxable_income": 34803,
      "tax": 7137.56
    }
  ]
}
```

---

## Running Unit Tests

```bash
pytest
```

With detailed output:

```bash
pytest -v
```

---

## Technology Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)
- [Requests](https://docs.python-requests.org/)
- [pytest](https://docs.pytest.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## Engineering Principles Used

- **Clean Architecture**: Separation of concerns across domain, service, and API layers
- **Single Responsibility**: Components follow SRP for maintainability
- **Environment Isolation**: `.env` and settings module for portability
- **OpenAPI-first**: Auto-generated API docs with validation
- **Testability**: Dependency injection and unit test coverage using `TestClient`

---
# Timebox:

1. Understanding of Problem statement - 10 min
2. Pseudo Code with Happy Path Scenario - 20 min
3. Architecture and Design Pattern - 10 min
4. Refactoring - 20 min
5. Code Changes and Exception Handling - 40 min
6. Manual Testing and bug fixing - 40 min
7. Validation - 20 min
8. Unit Testing - 20 min
9. Adding Missing Document Level Comments - 20 min
10. Review and Documentation - 45 min

Total : 245 min --> 4hr 5min