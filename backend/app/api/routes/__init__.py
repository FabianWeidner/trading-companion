from fastapi import APIRouter
from . import trades

api_router = APIRouter()
api_router.include_router(trades.router, prefix="/trades", tags=["trades"])
