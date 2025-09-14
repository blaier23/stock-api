import pytest
import requests
from http import HTTPStatus

BASE_URL = "http://localhost:8000"


@pytest.mark.integration
def test_post_and_get_stock_accumulates():
    """Check that POST actually stores and GET reflects the new amount."""

    # First reset by posting a small amount
    resp = requests.post(f"{BASE_URL}/stock/IBM", json={"amount": 1})
    assert resp.status_code == HTTPStatus.CREATED

    # Post again to accumulate
    resp = requests.post(f"{BASE_URL}/stock/IBM", json={"amount": 4})
    assert resp.status_code == HTTPStatus.CREATED

    # Now GET should show amount=5
    resp = requests.get(f"{BASE_URL}/stock/IBM")
    assert resp.status_code == HTTPStatus.OK
    data = resp.json()
    assert data["amount"] == 5


@pytest.mark.integration
def test_post_invalid_amount():
    """Posting 0 or negative should fail."""

    resp = requests.post(f"{BASE_URL}/stock/TSLA", json={"amount": 0})
    assert resp.status_code == HTTPStatus.BAD_REQUEST

    resp = requests.post(f"{BASE_URL}/stock/TSLA", json={"amount": -5})
    assert resp.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.integration
def test_post_invalid_json():
    """Non-integer amount should fail with 422."""

    resp = requests.post(f"{BASE_URL}/stock/NVDA", json={"amount": "five"})
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
def test_get_unknown_stock():
    """Fetching an unknown stock should still return a valid structure (mock depends on API)."""

    resp = requests.get(f"{BASE_URL}/stock/UNKNOWN")
    
    assert resp.status_code in [HTTPStatus.OK, HTTPStatus.BAD_GATEWAY]
