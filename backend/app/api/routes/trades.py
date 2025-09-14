from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import crud, schemas, models

router = APIRouter()


# CREATE
@router.post("/", response_model=schemas.TradeRead)
def create_trade(trade: schemas.TradeCreate, db: Session = Depends(get_db)):
    db_trade = models.Trade(**trade.model_dump())  # ✅ Pydantic v2
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade


# READ all
@router.get("/", response_model=List[schemas.TradeRead])
def read_trades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.trades.get_trades(db, skip=skip, limit=limit)


# READ one
@router.get("/{trade_id}", response_model=schemas.TradeRead)
def read_trade(trade_id: int, db: Session = Depends(get_db)):
    db_obj = crud.trades.get_trade(db, trade_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Trade not found")
    return db_obj


# UPDATE
@router.put("/{trade_id}", response_model=schemas.TradeRead)
def update_trade(
    trade_id: int, trade_in: schemas.TradeUpdate, db: Session = Depends(get_db)
):
    db_obj = crud.trades.get_trade(db, trade_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Trade not found")
    return crud.trades.update_trade(db, db_obj, trade_in)


# DELETE
@router.delete("/{trade_id}")
def delete_trade(trade_id: int, db: Session = Depends(get_db)):
    db_obj = crud.trades.get_trade(db, trade_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Trade not found")
    crud.trades.delete_trade(db, db_obj)
    return {"ok": True}
