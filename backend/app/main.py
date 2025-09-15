from fastapi import FastAPI
from app.api.routes import api_router
from app.db.session import engine
from app.db.base import Base

app = FastAPI(title="Trading Companion API")


Base.metadata.create_all(bind=engine)

app.include_router(api_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
