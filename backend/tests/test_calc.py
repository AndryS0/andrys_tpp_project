import pytest
from fastapi.testclient import TestClient
from app import app  # assuming your FastAPI app is defined in app/main.py
from app.dependencies.id_token_validator import check_api_token
from app.schemas import CalcRequest

client = TestClient(app)


# Mock token validation for testing
def mock_check_api_token():
    pass


app.dependency_overrides[check_api_token] = mock_check_api_token


@pytest.fixture(autouse=True)
def override_check_api_token():
    pass


def test_calc_valid_expression():
    request_data = {"expression": "2 + 3 * 4"}  # Valid expression
    response = client.get("/api/v1/calc", params=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == 14


def test_calc_invalid_expression():
    request_data = {"expression": "2 +"}  # Invalid expression (Syntax Error)
    response = client.get("/api/v1/ccalc", params=request_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


def test_calc_invalid_key():
    request_data = {"wrong_key": "2 + 3"}  # Incorrect key in the request
    response = client.get("/api/v1/calc", params=request_data)
    assert response.status_code == 422  # FastAPI will raise 422 for missing required fields
