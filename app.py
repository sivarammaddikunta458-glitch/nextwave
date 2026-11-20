import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template, request


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("CIVIC_PULSE_DB", BASE_DIR / "civic_pulse.db"))
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

STATUSES = ("Pending", "Saved Offline", "Sending", "Alert Sent", "Assistance Dispatched", "Resolved")
CATEGORIES = ("Medical Emergency", "Accident", "Personal Safety", "Other Emergency")


def db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with db_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL UNIQUE,
                emergency_contact_name TEXT,
                emergency_contact_phone TEXT,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                message TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                location_link TEXT,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL,
                last_error TEXT,
                attempts INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            """
        )


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def row_to_dict(row):
    return dict(row) if row else None


def send_sms(alert, user):
    """Send through a configured provider, or stay safely in demo mode.

    A production deployment should replace this adapter with the chosen
    operator/provider integration. No claim is made that SMS is free.
    """
    if os.getenv("CIVIC_PULSE_SMS_PROVIDER", "demo").lower() == "demo":
        return False, "Demo mode: configure an SMS provider to transmit alerts."
    # Provider integrations belong here. Keeping the boundary explicit avoids
    # pretending a browser or Flask server can send carrier SMS by itself.
    return False, "SMS provider integration is not configured."


def alert_payload(row):
    payload = row_to_dict(row)
    if payload:
        payload["map_url"] = (
            f"https://www.openstreetmap.org/?mlat={payload['latitude']}&mlon={payload['longitude']}#map=18/{payload['latitude']}/{payload['longitude']}"
            if payload["latitude"] is not None and payload["longitude"] is not None
            else None
        )
    return payload


@app.get("/")
def index():
    return render_template("index.html", categories=CATEGORIES, statuses=STATUSES)


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "service": "Civic Pulse", "sms_mode": os.getenv("CIVIC_PULSE_SMS_PROVIDER", "demo")})


@app.post("/api/users")
def create_user():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    phone = str(data.get("phone", "")).strip()
    if not name or not phone:
        return jsonify({"error": "Name and phone number are required."}), 400
    try:
        with db_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO users (name, phone, emergency_contact_name, emergency_contact_phone, created_at) VALUES (?, ?, ?, ?, ?)",
                (name, phone, data.get("emergency_contact_name"), data.get("emergency_contact_phone"), now_iso()),
            )
            return jsonify({"id": cursor.lastrowid, "message": "Registration saved."}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "That phone number is already registered."}), 409


@app.post("/api/alerts")
def create_alert():
    data = request.get_json(silent=True) or {}
    try:
        user_id = int(data["user_id"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "A valid user_id is required."}), 400
    category = str(data.get("category", "")).strip()
    if category not in CATEGORIES:
        return jsonify({"error": "Choose a valid emergency category."}), 400
    with db_connection() as connection:
        user = connection.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if not user:
            return jsonify({"error": "Register the citizen before creating an alert."}), 404
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        location_link = data.get("location_link")
        message = data.get("message") or f"CIVIC PULSE ALERT: {category} reported by {user['name']} ({user['phone']})."
        cursor = connection.execute(
            "INSERT INTO alerts (user_id, category, message, latitude, longitude, location_link, created_at, status, attempts) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)",
            (user_id, category, message, latitude, longitude, location_link, now_iso(), "Pending"),
        )
        alert_id = cursor.lastrowid
        alert = connection.execute("SELECT alerts.*, users.name, users.phone FROM alerts JOIN users ON users.id = alerts.user_id WHERE alerts.id = ?", (alert_id,)).fetchone()
        sent, error = send_sms(alert, user)
        new_status = "Alert Sent" if sent else "Saved Offline"
        connection.execute("UPDATE alerts SET status = ?, attempts = attempts + 1, last_error = ? WHERE id = ?", (new_status, None if sent else error, alert_id))
        alert = connection.execute("SELECT alerts.*, users.name, users.phone FROM alerts JOIN users ON users.id = alerts.user_id WHERE alerts.id = ?", (alert_id,)).fetchone()
        return jsonify({"alert": alert_payload(alert), "sms_sent": sent, "notice": error}), 201


@app.get("/api/alerts")
def list_alerts():
    with db_connection() as connection:
        rows = connection.execute("SELECT alerts.*, users.name, users.phone FROM alerts JOIN users ON users.id = alerts.user_id ORDER BY alerts.created_at DESC").fetchall()
    return jsonify([alert_payload(row) for row in rows])


@app.patch("/api/alerts/<int:alert_id>")
def update_alert(alert_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    if status not in STATUSES:
        return jsonify({"error": "Invalid alert status."}), 400
    with db_connection() as connection:
        cursor = connection.execute("UPDATE alerts SET status = ? WHERE id = ?", (status, alert_id))
        if cursor.rowcount == 0:
            return jsonify({"error": "Alert not found."}), 404
    return jsonify({"message": "Alert status updated."})


@app.post("/api/alerts/retry")
def retry_alerts():
    with db_connection() as connection:
        pending = connection.execute("SELECT alerts.*, users.name, users.phone FROM alerts JOIN users ON users.id = alerts.user_id WHERE alerts.status IN ('Pending', 'Saved Offline')").fetchall()
        sent_count = 0
        for alert in pending:
            user = connection.execute("SELECT * FROM users WHERE id = ?", (alert["user_id"],)).fetchone()
            sent, error = send_sms(alert, user)
            connection.execute("UPDATE alerts SET status = ?, attempts = attempts + 1, last_error = ? WHERE id = ?", ("Alert Sent" if sent else "Saved Offline", None if sent else error, alert["id"]))
            sent_count += int(sent)
    return jsonify({"checked": len(pending), "sent": sent_count})


initialize_database()

if __name__ == "__main__":
    app.run(debug=True)
