# Note: This project was developed with selective assistance of AI-based tools
# (e.g., for debugging, architectural discussion, and explanation).
# All core logic, design decisions, and final implementation choices
# were made and reviewed by the author.

import sqlite3
import os
from datetime import datetime, UTC
from flask import Flask, render_template, request, redirect, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import jsonify, request  

app = Flask(__name__)
app.secret_key = "dev-secret-change-later"

DATABASE = "pomodoro.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated


def api_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("user_id") is None:
            return jsonify({"error": "login required"}), 401
        return f(*args, **kwargs)
    return decorated


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = ON;")

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_type TEXT NOT NULL CHECK(session_type IN ('focus', 'short_break', 'long_break')),
            duration_seconds INTEGER NOT NULL CHECK(duration_seconds >= 0),
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)

    db.commit()
    db.close()


@app.route("/")
def index():
    return render_template("timer.html", user_id=session.get("user_id"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    confirmation = request.form.get("confirmation") or ""

    if not username:
        return "must provide username", 400
    if not password:
        return "must provide password", 400
    if password != confirmation:
        return "passwords must match", 400

    pw_hash = generate_password_hash(password)
    created_at = datetime.now(UTC).isoformat()

    db = get_db()
    try:
        cur = db.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
            (username, pw_hash, created_at),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return "username already exists", 400

    session.clear()
    session["user_id"] = cur.lastrowid
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    
    session.clear()

    if request.method == "GET":
        return render_template("login.html")

    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""

    if not username:
        return "must provide username", 400
    if not password:
        return "must provide password", 400

    db = get_db()
    row = db.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (username,),
    ).fetchone()

    if row is None or not check_password_hash(row["password_hash"], password):
        return "invalid username and/or password", 403

    session["user_id"] = row["id"]
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/history")
@login_required
def history():
    db = get_db()

    # last 50 focus sessions
    rows = db.execute("""
        SELECT id, duration_seconds, created_at
        FROM sessions
        WHERE user_id = ? AND session_type = 'focus'
        ORDER BY id DESC
        LIMIT 50
    """, (session["user_id"],)).fetchall()

    stats = db.execute("""
        SELECT
          COUNT(*) AS focus_count,
          COALESCE(SUM(duration_seconds), 0) AS total_seconds
        FROM sessions
        WHERE user_id = ? AND session_type = 'focus'
    """, (session["user_id"],)).fetchone()

    focus_count = int(stats["focus_count"])
    total_minutes = int(stats["total_seconds"] // 60)
    blocks_completed = focus_count // 4
    remainder = focus_count % 4

    return render_template(
        "history.html",
        rows=rows,
        focus_count=focus_count,
        total_minutes=total_minutes,
        blocks_completed=blocks_completed,
        remainder=remainder
    )


@app.route("/api/log", methods=["POST"])
@api_login_required
def api_log():
    data = request.get_json(silent=True) or {}
    session_type = data.get("type", "focus")
    duration_seconds = int(data.get("duration_seconds", 25 * 60))
    print("api_log hit by user:", session.get("user_id"), "data:", data)

    if session_type not in ("focus", "short_break", "long_break"):
        return jsonify({"error": "invalid session_type"}), 400
    if duration_seconds < 0:
        return jsonify({"error": "invalid duration"}), 400

    db = get_db()
    db.execute(
        """
        INSERT INTO sessions (user_id, session_type, duration_seconds, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (session["user_id"], session_type, duration_seconds, datetime.now(UTC).isoformat()),
    )
    db.commit()

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)