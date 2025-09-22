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

    # DELETE (API gibt gelöschten Trade zurück)
    response = client.delete(f"/trades/{trade_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == trade_id
    assert data["symbol"] == "AAPL"


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
    body = response.json()
    assert any(err["loc"][-1] == "qty" for err in body["detail"])


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
    body = response.json()
    assert any(err["loc"][-1] == "price" for err in body["detail"])


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


def test_close_trade():
    response = client.post(
        "/trades/",
        json={
            "symbol": "AAPL",
            "side": "LONG",
            "strategy": "Breakout",
            "qty": 1.0,
            "price": 190.0,
        },
    )
    assert response.status_code == 200
    trade = response.json()
    trade_id = trade["id"]

    response = client.post(
        f"/trades/{trade_id}/close", json={"exit_price": 195.0, "exit_reason": "Target"}
    )
    assert response.status_code == 200
    closed_trade = response.json()

    assert closed_trade["id"] == trade_id
    assert closed_trade["exit_price"] == 195.0
    assert closed_trade["exit_reason"] == "Target"
    assert closed_trade["closed_at"] is not None

    # re-check via GET
    response = client.get(f"/trades/{trade_id}")
    assert response.status_code == 200
    trade_after = response.json()
    assert trade_after["exit_price"] == 195.0
    assert trade_after["closed_at"] is not None
