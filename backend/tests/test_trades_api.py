from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_read_update_delete_trade():
    # CREATE
    response = client.post(
        "/trades/",
        json={
            "symbol": "AAPL",
            "side": "LONG",
            "strategy": "Breakout",
            "qty": 1.0,
            "price": 190.0,
            "screenshot_url": "/uploads/trades/test.png",
        },
    )
    assert response.status_code == 200
    data = response.json()
    trade_id = data["id"]

    # READ
    response = client.get(f"/trades/{trade_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"

    # UPDATE
    response = client.put(
        f"/trades/{trade_id}",
        json={"strategy": "Reversal"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["strategy"] == "Reversal"

    # DELETE
    response = client.delete(f"/trades/{trade_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True


def test_create_trade_with_invalid_qty():
    response = client.post(
        "/trades/",
        json={
            "symbol": "AAPL",
            "side": "LONG",
            "strategy": "Breakout",
            "qty": -5,  # invalid
            "price": 190.0,
        },
    )
    assert response.status_code == 422


def test_create_trade_with_invalid_side():
    response = client.post(
        "/trades/",
        json={
            "symbol": "AAPL",
            "side": "INVALID",  # invalid
            "strategy": "Breakout",
            "qty": 1.0,
            "price": 190.0,
        },
    )
    assert response.status_code == 422


def test_get_nonexistent_trade():
    response = client.get("/trades/999999")
    assert response.status_code == 404


def test_delete_twice():
    # CREATE
    response = client.post(
        "/trades/",
        json={
            "symbol": "TSLA",
            "side": "LONG",
            "strategy": "Scalping",
            "qty": 1.0,
            "price": 250.0,
        },
    )
    trade_id = response.json()["id"]

    # DELETE once
    response = client.delete(f"/trades/{trade_id}")
    assert response.status_code == 200

    # DELETE again
    response = client.delete(f"/trades/{trade_id}")
    assert response.status_code == 404


def test_create_trade_with_zero_qty():
    response = client.post(
        "/trades/",
        json={
            "symbol": "AAPL",
            "side": "LONG",
            "strategy": "Breakout",
            "qty": 0,  # invalid
            "price": 190.0,
        },
    )
    assert response.status_code == 422
    assert "Quantity must be positive" in response.text


def test_create_trade_with_zero_price():
    response = client.post(
        "/trades/",
        json={
            "symbol": "AAPL",
            "side": "LONG",
            "strategy": "Breakout",
            "qty": 1.0,
            "price": 0,  # invalid
        },
    )
    assert response.status_code == 422
    assert "Price must be positive" in response.text


def test_create_trade_without_screenshot_url():
    response = client.post(
        "/trades/",
        json={
            "symbol": "AAPL",
            "side": "SHORT",
            "strategy": "Reversal",
            "qty": 2.0,
            "price": 150.0,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["screenshot_url"] is None
    assert data["side"] == "SHORT"
    assert data["symbol"] == "AAPL"
