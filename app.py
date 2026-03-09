from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "promptvault-secret-key"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "prompts.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = get_db_connection()
    prompts = conn.execute(
        "SELECT id, title, category, description, created_at FROM prompts ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return render_template("home.html", prompts=prompts)


@app.route("/add", methods=["GET", "POST"])
def add_prompt():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()

        if not title or not category or not description:
            flash("All fields are required.", "error")
            return render_template("add_prompt.html", title=title, category=category, description=description)

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO prompts (title, category, description) VALUES (?, ?, ?)",
            (title, category, description),
        )
        conn.commit()
        conn.close()

        flash("Prompt saved successfully!", "success")
        return redirect(url_for("home"))

    return render_template("add_prompt.html")


@app.route("/search")
def search_prompts():
    query = request.args.get("q", "").strip()
    prompts = []

    if query:
        like_query = f"%{query}%"
        conn = get_db_connection()
        prompts = conn.execute(
            """
            SELECT id, title, category, description, created_at
            FROM prompts
            WHERE title LIKE ? OR category LIKE ? OR description LIKE ?
            ORDER BY created_at DESC
            """,
            (like_query, like_query, like_query),
        ).fetchall()
        conn.close()

    return render_template("search.html", prompts=prompts, query=query)


init_db()

if __name__ == "__main__":
    app.run(debug=True)
