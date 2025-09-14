from sqlalchemy.orm import Session
from app import models, schemas


def create_trade(db: Session, trade_in: schemas.TradeCreate) -> models.Trade:
    db_trade = models.Trade(**trade_in.model_dump())  # ✅ Pydantic v2
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade


def get_trades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trade).offset(skip).limit(limit).all()


def get_trade(db: Session, trade_id: int):
    return db.query(models.Trade).filter(models.Trade.id == trade_id).first()


def update_trade(
    db: Session, db_obj: models.Trade, trade_in: schemas.TradeUpdate
) -> models.Trade:
    update_data = trade_in.model_dump(exclude_unset=True)  # ✅ Pydantic v2
    for key, value in update_data.items():
        setattr(db_obj, key, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_trade(db: Session, db_obj: models.Trade):
    db.delete(db_obj)
    db.commit()
