from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings

# Engine erzeugen
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # wichtig für SQLite
)

# SessionLocal als Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
