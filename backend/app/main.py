from fastapi import FastAPI
from app.api.routes import api_router
from app.db.init_db import init_db
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Trading Companion API")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.mount("/uploads", StaticFiles(directory="backend/uploads"), name="uploads")

app.include_router(api_router)
