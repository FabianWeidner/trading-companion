import typer
import os
from app.db.base import Base
from app.db.session import engine
from app.db.init_db import init_db, DB_FILE

app = typer.Typer(help="Management CLI für Trading Companion")


@app.command()
def init():
    """Initialisiert die Datenbank (fragt bei bestehender Datei nach)."""
    init_db()


@app.command()
def reset(
    confirm: bool = typer.Option(
        False, "--confirm", "-c", help="Bestätigung zum Löschen"
    )
):
    """Löscht die Datenbank und erstellt sie neu."""
    if not os.path.exists(DB_FILE):
        typer.echo("ℹ️ Keine bestehende Datenbank gefunden.")
    else:
        if not confirm:
            typer.confirm(
                f"⚠️ Soll die bestehende Datenbank '{DB_FILE}' gelöscht werden?",
                abort=True,
            )
        os.remove(DB_FILE)
        typer.echo(f"🗑️ Datenbank '{DB_FILE}' gelöscht.")

    Base.metadata.create_all(bind=engine)
    typer.echo("✅ Datenbank neu erstellt!")


if __name__ == "__main__":
    app()
