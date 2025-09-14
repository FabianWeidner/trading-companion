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
    assert response.status_code == 200, response.text
    trade = response.json()
    trade_id = trade["id"]
    assert trade["symbol"] == "AAPL"

    # READ
    response = client.get(f"/trades/{trade_id}")
    assert response.status_code == 200
    trade = response.json()
    assert trade["id"] == trade_id
    assert trade["symbol"] == "AAPL"

    # UPDATE
    response = client.put(
        f"/trades/{trade_id}",
        json={"strategy": "Reversal"},
    )
    assert response.status_code == 200
    trade = response.json()
    assert trade["strategy"] == "Reversal"

    # DELETE
    response = client.delete(f"/trades/{trade_id}")
    assert response.status_code == 200
    result = response.json()
    assert result["ok"] is True

    # Ensure it's gone
    response = client.get(f"/trades/{trade_id}")
    assert response.status_code == 404
