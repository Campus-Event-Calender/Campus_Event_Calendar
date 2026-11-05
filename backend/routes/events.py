import re
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request
from ..database import get_db
from ..models import all_events, event_with_counts

events_bp = Blueprint("events", __name__, url_prefix="/api/events")
EVENT_FIELDS = ("title", "description", "category", "venue", "start_time", "end_time", "capacity")
REQUIRED_FIELDS = ("title", "start_time", "end_time")


def _validate_event(data, current=None):
    if not isinstance(data, dict):
        return None, "Request body must be a JSON object"

    unknown = set(data) - set(EVENT_FIELDS)
    if unknown:
        return None, f"Unknown fields: {', '.join(sorted(unknown))}"
    if current is None:
        missing = [field for field in REQUIRED_FIELDS if not data.get(field)]
        if missing:
            return None, f"Missing fields: {', '.join(missing)}"
    elif not data:
        return None, "No fields to update"

    values = {field: current[field] for field in EVENT_FIELDS} if current else {
        "title": None,
        "description": "",
        "category": "Other",
        "venue": "Campus",
        "start_time": None,
        "end_time": None,
        "capacity": 100,
    }
    values.update(data)

    for field in ("title", "start_time", "end_time"):
        value = values[field]
        if not isinstance(value, str) or not value.strip():
            return None, f"{field} is required"
        values[field] = value.strip()

    for field in ("description", "category", "venue"):
        if not isinstance(values[field], str):
            return None, f"{field} must be a string"

    try:
        start = datetime.fromisoformat(values["start_time"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(values["end_time"].replace("Z", "+00:00"))
        if (start.tzinfo is None) != (end.tzinfo is None):
            return None, "start_time and end_time must use consistent time zones"
        if start.tzinfo is not None:
            start = start.astimezone(timezone.utc)
            end = end.astimezone(timezone.utc)
    except ValueError:
        return None, "start_time and end_time must be valid ISO date-times"
    if end <= start:
        return None, "end_time must be later than start_time"

    capacity = values["capacity"]
    if type(capacity) is int:
        parsed_capacity = capacity
    elif isinstance(capacity, str) and re.fullmatch(r"[0-9]+", capacity.strip()):
        parsed_capacity = int(capacity.strip())
    else:
        return None, "capacity must be a positive integer"
    if parsed_capacity < 1:
        return None, "capacity must be a positive integer"
    values["capacity"] = parsed_capacity

    return values, None

@events_bp.get("")
def list_events():
    conn = get_db()
    data = all_events(conn)
    conn.close()
    return jsonify(data)

@events_bp.get("/<int:event_id>")
def get_event(event_id):
    conn = get_db()
    data = event_with_counts(conn, event_id)
    conn.close()
    if not data:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(data)

@events_bp.post("")
def create_event():
    data = request.get_json(silent=True) or {}
    values, error = _validate_event(data)
    if error:
        return jsonify({"error": error}), 400

    conn = get_db()
    cur = conn.execute("""INSERT INTO events
        (title, description, category, venue, start_time, end_time, capacity)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        tuple(values[field] for field in EVENT_FIELDS))
    conn.commit()
    result = event_with_counts(conn, cur.lastrowid)
    conn.close()
    return jsonify(result), 201

@events_bp.put("/<int:event_id>")
def update_event(event_id):
    data = request.get_json(silent=True) or {}
    conn = get_db()
    conn.execute("BEGIN IMMEDIATE")
    current = event_with_counts(conn, event_id)
    if not current:
        conn.rollback()
        conn.close()
        return jsonify({"error": "Event not found"}), 404

    values, error = _validate_event(data, current)
    if error:
        conn.rollback()
        conn.close()
        return jsonify({"error": error}), 400

    rsvp_count = conn.execute(
        "SELECT COUNT(*) FROM rsvps WHERE event_id=? AND status='confirmed'",
        (event_id,),
    ).fetchone()[0]
    if values["capacity"] < rsvp_count:
        conn.rollback()
        conn.close()
        return jsonify({"error": "capacity cannot be less than the number of confirmed RSVPs"}), 400

    conn.execute("""UPDATE events SET title=?, description=?, category=?, venue=?,
                    start_time=?, end_time=?, capacity=? WHERE id=?""",
                 tuple(values[field] for field in EVENT_FIELDS) + (event_id,))
    conn.commit()
    result = event_with_counts(conn, event_id)
    conn.close()
    return jsonify(result)

@events_bp.delete("/<int:event_id>")
def delete_event(event_id):
    conn = get_db()
    if not event_with_counts(conn, event_id):
        conn.close()
        return jsonify({"error": "Event not found"}), 404
    cur = conn.execute("DELETE FROM events WHERE id=?", (event_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Event deleted"})
