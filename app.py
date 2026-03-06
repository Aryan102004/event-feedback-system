import os
import sqlite3
import csv
from flask import Response
from datetime import datetime
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey123"   # Change in production

# ==========================================
# DATABASE CONFIGURATION (Absolute Path)
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "feedback.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            event TEXT NOT NULL,

            q1 INTEGER NOT NULL,
            q2 INTEGER NOT NULL,
            q3 INTEGER NOT NULL,
            q4 INTEGER NOT NULL,
            q5 INTEGER NOT NULL,
            q6 INTEGER NOT NULL,
            q7 INTEGER NOT NULL,
            q8 INTEGER NOT NULL,

            liked TEXT NOT NULL,
            improvement TEXT NOT NULL,
            suggestion TEXT NOT NULL,

            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Initialize DB on startup
init_db()


# ==========================================
# ADMIN CREDENTIALS (Simple Version)
# ==========================================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ==========================================
# PUBLIC ROUTES
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/events")
def events():
    return render_template("events.html")


@app.route("/feedback")
def feedback():
    success = request.args.get("success")
    return render_template("feedback.html", success=success)


# ==========================================
# SUBMIT FEEDBACK (CREATE)
# ==========================================

@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():

    name = request.form["name"]
    email = request.form["email"]
    event = request.form["event"]

    q1 = request.form["q1"]
    q2 = request.form["q2"]
    q3 = request.form["q3"]
    q4 = request.form["q4"]
    q5 = request.form["q5"]
    q6 = request.form["q6"]
    q7 = request.form["q7"]
    q8 = request.form["q8"]

    liked = request.form["liked"]
    improvement = request.form["improvement"]
    suggestion = request.form["suggestion"]

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO feedback
        (name, email, event,
         q1, q2, q3, q4, q5, q6, q7, q8,
         liked, improvement, suggestion, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name, email, event,
        q1, q2, q3, q4, q5, q6, q7, q8,
        liked, improvement, suggestion,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("feedback", success=1))


# ==========================================
# ADMIN LOGIN
# ==========================================

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect("/view_feedback")
        else:
            return "Invalid Credentials"

    return render_template("admin_login.html")


# ==========================================
# VIEW ALL FEEDBACK (ADMIN ONLY)
# ==========================================

@app.route("/view_feedback")
def view_feedback():

    if not session.get("admin_logged_in"):
        return redirect("/admin_login")

    conn = get_db_connection()
    feedbacks = conn.execute(
        "SELECT * FROM feedback ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("view_feedback.html", feedbacks=feedbacks)

@app.route("/export_csv/<event_name>")
def export_csv(event_name):

    if not session.get("admin_logged_in"):
        return redirect("/admin_login")

    conn = get_db_connection()

    feedbacks = conn.execute(
        "SELECT * FROM feedback WHERE event = ? ORDER BY id DESC",
        (event_name,)
    ).fetchall()

    conn.close()

    if not feedbacks:
        return "No feedback available for this event."

    def generate():
        yield ','.join([
            "ID", "Name", "Email", "Event",
            "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8",
            "Liked", "Improvement", "Suggestion", "Submitted At"
        ]) + '\n'

        for fb in feedbacks:
            yield ','.join([
                str(fb["id"]),
                fb["name"],
                fb["email"],
                fb["event"],
                str(fb["q1"]),
                str(fb["q2"]),
                str(fb["q3"]),
                str(fb["q4"]),
                str(fb["q5"]),
                str(fb["q6"]),
                str(fb["q7"]),
                str(fb["q8"]),
                fb["liked"].replace(',', ' '),
                fb["improvement"].replace(',', ' '),
                fb["suggestion"].replace(',', ' '),
                fb["created_at"]
            ]) + '\n'

    safe_filename = event_name.replace(" ", "_")

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            f"attachment;filename={safe_filename}_feedback.csv"
        }
    )
# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect("/")


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)