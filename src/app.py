from datetime import datetime, timedelta, timezone
from pathlib import Path

from flask import Flask, render_template
from markdown2 import markdown

BRAZIL_TZ = timezone(timedelta(hours=-3))


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Store the application start time
    app_uptime = datetime.now(tz=BRAZIL_TZ)
    app.config["APP_UPTIME"] = app_uptime

    return app


app = create_app()


@app.route("/")
def home() -> str:
    """Render the README.md content as the home page."""
    with Path("../README.md").open() as f:
        readme_content = f.read()
        html = markdown(readme_content, extras=["fenced-code-blocks"])
    return render_template("home.html", html=html)


@app.route("/health")
def health() -> str:
    """Health check endpoint."""
    timestamp = datetime.now(tz=BRAZIL_TZ)
    uptime = timestamp - app.config["APP_UPTIME"]

    timestamp = timestamp.isoformat()
    uptime = (
        f"{uptime.days}d "
        f"{uptime.seconds // 3600}h "
        f"{(uptime.seconds // 60) % 60}m "
        f"{uptime.seconds % 60}s"
    )

    response = {
        "status": "healthy",
        "database": True,  # Simulated database status
        "uptime": uptime,
        "timestamp": timestamp,
    }
    return response, 200
