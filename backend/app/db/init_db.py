import os
from app.db.base import Base
from app.db.session import engine

DB_FILE = "backend/app.db"  # falls du SQLite nutzt


def init_db():
    """Initialisiert die Datenbank, fragt bei bestehender Datei nach."""
    if os.path.exists(DB_FILE):
        answer = input(
            f"⚠️ Datenbank '{DB_FILE}' existiert bereits. Neu erstellen? (y/N): "
        )
        if answer.lower() != "y":
            print("❌ Abgebrochen – bestehende Datenbank bleibt erhalten.")
            return
        os.remove(DB_FILE)
        print(f"🗑️ Alte Datenbank '{DB_FILE}' gelöscht.")

    print("➡️ Erstelle Tabellen …")
    Base.metadata.create_all(bind=engine)
    print("✅ Datenbank wurde erfolgreich initialisiert!")


if __name__ == "__main__":
    init_db()
