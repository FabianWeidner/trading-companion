from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "backend" / "dev.db"


class Settings:
    DATABASE_URL: str = f"sqlite:///{DB_PATH}"


# hier die Instanz bereitstellen:
settings = Settings()
