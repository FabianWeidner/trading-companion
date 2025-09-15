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
    trade = response.json()
    trade_id = trade["id"]

    # READ
    response = client.get(f"/trades/{trade_id}")
    assert response.status_code == 200
    assert response.json()["symbol"] == "AAPL"

    # UPDATE
    response = client.put(
        f"/trades/{trade_id}",
        json={"qty": 2.0},
    )
    assert response.status_code == 200
    assert response.json()["qty"] == 2.0

    # DELETE
    response = client.delete(f"/trades/{trade_id}")
    assert response.status_code == 200
    assert response.json()["ok"] is True


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
    assert response.status_code == 422  # Unprocessable Entity


def test_create_trade_with_invalid_side():
    response = client.post(
        "/trades/",
        json={
            "symbol": "AAPL",
            "side": "UP",  # invalid side, only LONG/SHORT allowed
            "strategy": "Breakout",
            "qty": 1.0,
            "price": 190.0,
        },
    )
    assert response.status_code == 422


def test_get_nonexistent_trade():
    response = client.get("/trades/99999")
    assert response.status_code == 404


def test_delete_twice():
    # create trade
    response = client.post(
        "/trades/",
        json={
            "symbol": "MSFT",
            "side": "SHORT",
            "strategy": "Reversal",
            "qty": 1.0,
            "price": 300.0,
        },
    )
    trade_id = response.json()["id"]

    # delete once
    response = client.delete(f"/trades/{trade_id}")
    assert response.status_code == 200

    # delete again
    response = client.delete(f"/trades/{trade_id}")
    assert response.status_code == 404
