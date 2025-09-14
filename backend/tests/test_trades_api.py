import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_get_trades_empty_db():
    """
    Testet den GET /trades Endpoint mit leerer Datenbank.
    Erwartung: Antwort ist 200 OK und eine leere Liste.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/trades")
    assert response.status_code == 200
    assert response.json() == []
