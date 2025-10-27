import psycopg2
from flask import g

from .settings import Settings


def get_db():
    """Get a database connection from the application context."""
    if "db" not in g:
        g.db = psycopg2.connect(
            dbname=Settings.DB_NAME,
            user=Settings.DB_USER,
            password=Settings.DB_PASSWORD,
            host=Settings.DB_HOST,
            port=Settings.DB_PORT,
        )
    return g.db


def close_db(e=None):
    """Close the database connection if it exists."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Initialize the database connection and register teardown function."""
    app.teardown_appcontext(close_db)
