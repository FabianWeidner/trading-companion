from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas


def create_trade(db: Session, trade_in: schemas.TradeCreate) -> models.Trade:
    db_trade = models.Trade(**trade_in.model_dump())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade


def get_trades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trade).offset(skip).limit(limit).all()


def get_trade(db: Session, trade_id: int):
    return db.query(models.Trade).filter(models.Trade.id == trade_id).first()


def update_trade(db: Session, trade_id: int, trade_in: schemas.TradeUpdate):
    db_trade = get_trade(db, trade_id)
    if not db_trade:
        return None
    update_data = trade_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_trade, key, value)
    db.commit()
    db.refresh(db_trade)
    return db_trade


def delete_trade(db: Session, trade_id: int):
    db_trade = get_trade(db, trade_id)
    if not db_trade:
        return None
    db.delete(db_trade)
    db.commit()
    return True


def close_trade(
    db: Session, trade_id: int, close_in: schemas.TradeClose
) -> models.Trade | None:
    db_obj = db.query(models.Trade).filter(models.Trade.id == trade_id).first()
    if not db_obj:
        return None

    db_obj.exit_price = close_in.exit_price
    db_obj.exit_reason = close_in.exit_reason
    db_obj.closed_at = datetime.utcnow()

    db.commit()
    db.refresh(db_obj)
    return db_obj
