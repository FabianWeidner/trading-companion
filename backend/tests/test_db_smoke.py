from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.trade import Trade


def test_insert_and_read_trade():
    with SessionLocal() as db:
        t = Trade(
            symbol="AAPL",
            side="LONG",
            strategy="Breakout",
            qty=1.0,
            price=190.0,
            screenshot_url="/uploads/trades/1.png",
        )
        db.add(t)
        db.commit()
        db.refresh(t)

        assert t.id is not None

        row = db.execute(select(Trade).where(Trade.id == t.id)).scalar_one()
        assert row.symbol == "AAPL"
        assert row.strategy == "Breakout"
