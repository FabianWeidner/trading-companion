from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
import shutil
from uuid import uuid4

from app.db.session import get_db
from app import crud, schemas

router = APIRouter()

UPLOAD_DIR = "backend/uploads/trades"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=schemas.TradeRead)
def create_trade(trade: schemas.TradeCreate, db: Session = Depends(get_db)):
    return crud.trades.create_trade(db=db, trade_in=trade)


@router.get("/", response_model=list[schemas.TradeRead])
def read_trades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.trades.get_trades(db, skip=skip, limit=limit)


@router.get("/{trade_id}", response_model=schemas.TradeRead)
def read_trade(trade_id: int, db: Session = Depends(get_db)):
    db_obj = crud.trades.get_trade(db, trade_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Trade not found")
    return db_obj


@router.put("/{trade_id}", response_model=schemas.TradeRead)
def update_trade(
    trade_id: int, trade: schemas.TradeUpdate, db: Session = Depends(get_db)
):
    db_obj = crud.trades.update_trade(db=db, trade_id=trade_id, trade_in=trade)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Trade not found")
    return db_obj


@router.delete("/{trade_id}", response_model=schemas.TradeRead)
def delete_trade(trade_id: int, db: Session = Depends(get_db)):
    db_obj = crud.trades.delete_trade(db=db, trade_id=trade_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Trade not found")
    return db_obj


@router.post("/{trade_id}/screenshot", response_model=schemas.TradeRead)
def upload_trade_screenshot(
    trade_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    trade = crud.trades.get_trade(db, trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    ext = file.filename.split(".")[-1]
    filename = f"trade_{trade_id}_{uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    trade.screenshot_url = f"/uploads/{filename}"
    db.commit()
    db.refresh(trade)

    return trade


@router.post("/{trade_id}/close", response_model=schemas.TradeRead)
def close_trade(
    trade_id: int,
    close_in: schemas.TradeClose,
    db: Session = Depends(get_db),
):
    db_obj = crud.trades.close_trade(db, trade_id, close_in)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Trade not found")
    return db_obj
