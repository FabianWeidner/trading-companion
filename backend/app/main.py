from fastapi import FastAPI
from app.api.routes import api_router

app = FastAPI(title="Trading Companion API")

app.include_router(api_router)
