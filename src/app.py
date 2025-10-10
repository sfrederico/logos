from pathlib import Path

from flask import Flask, render_template
from markdown2 import markdown

app = Flask(__name__)


@app.route("/")
def home() -> str:
    """Render the README.md content as the home page."""
    with Path("../README.md").open() as f:
        readme_content = f.read()
        html = markdown(readme_content, extras=["fenced-code-blocks"])
    return render_template("home.html", html=html)
