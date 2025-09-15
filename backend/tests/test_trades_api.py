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

    # READ one
    response = client.get(f"/trades/{trade_id}")
    assert response.status_code == 200
    assert response.json()["symbol"] == "AAPL"

    # UPDATE
    response = client.put(f"/trades/{trade_id}", json={"strategy": "Reversal"})
    assert response.status_code == 200
    assert response.json()["strategy"] == "Reversal"

    # DELETE
    response = client.delete(f"/trades/{trade_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


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


def test_get_nonexistent_trade():
    response = client.get("/trades/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Trade not found"


def test_delete_twice():
    # Create
    response = client.post(
        "/trades/",
        json={
            "symbol": "TSLA",
            "side": "SHORT",
            "strategy": "Momentum",
            "qty": 2,
            "price": 250.0,
        },
    )
    trade_id = response.json()["id"]

    # First delete
    response = client.delete(f"/trades/{trade_id}")
    assert response.status_code == 200

    # Second delete should fail
    response = client.delete(f"/trades/{trade_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Trade not found"
