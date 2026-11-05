import sqlite3
from pathlib import Path
from flask import current_app, has_app_context

DB_PATH = Path(__file__).resolve().parent / "campus_events.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    category TEXT NOT NULL DEFAULT 'Other',
    venue TEXT NOT NULL DEFAULT 'Campus',
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    capacity INTEGER NOT NULL DEFAULT 100,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rsvps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    student_name TEXT NOT NULL,
    student_email TEXT NOT NULL,
    student_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'confirmed',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, student_email),
    FOREIGN KEY(event_id) REFERENCES events(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    student_email TEXT NOT NULL,
    attended INTEGER NOT NULL DEFAULT 1,
    marked_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, student_email),
    FOREIGN KEY(event_id) REFERENCES events(id) ON DELETE CASCADE
);
"""

def get_db(path=None):
    if path is None and has_app_context():
        path = current_app.config.get("DATABASE")
    conn = sqlite3.connect(path or DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(path=None, seed=True):
    conn = get_db(path)
    conn.executescript(SCHEMA)
    if seed and conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 0:
        seed_sample_data(conn)
    conn.commit()
    conn.close()

def seed_sample_data(conn):
    events = [
        ("AI & Machine Learning Workshop", "Hands-on introduction to modern AI tools and workflows.", "Workshop", "Innovation Lab", "2026-11-05T10:00:00", "2026-11-05T13:00:00", 120),
        ("Campus Hackathon 2026", "Build a useful prototype with your team in a 24-hour challenge.", "Hackathon", "Main Auditorium", "2026-11-12T09:00:00", "2026-11-13T09:00:00", 250),
        ("Tech Talk: Future of Cloud", "Industry speaker session covering cloud engineering and careers.", "Seminar", "Seminar Hall A", "2026-11-18T15:00:00", "2026-11-18T17:00:00", 150),
        ("Cultural Fest", "Music, dance, theatre and student club performances.", "Cultural", "Open Air Theatre", "2026-11-22T16:00:00", "2026-11-22T21:00:00", 500),
        ("Inter-College Basketball", "Annual inter-college basketball tournament.", "Sports", "University Sports Complex", "2026-11-28T09:00:00", "2026-11-28T16:00:00", 300),
    ]
    cur = conn.cursor()
    cur.executemany("""INSERT INTO events
        (title, description, category, venue, start_time, end_time, capacity)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", events)

    event_ids = [r[0] for r in cur.execute("SELECT id FROM events ORDER BY id").fetchall()]
    sample_rsvps = [
        (event_ids[0], "Aarav Sharma", "aarav@example.com", "STU001"),
        (event_ids[0], "Meera Rao", "meera@example.com", "STU002"),
        (event_ids[1], "Riya Patel", "riya@example.com", "STU003"),
        (event_ids[1], "Kiran Kumar", "kiran@example.com", "STU004"),
        (event_ids[1], "Ananya Singh", "ananya@example.com", "STU005"),
        (event_ids[2], "Dev Nair", "dev@example.com", "STU006"),
        (event_ids[3], "Isha Verma", "isha@example.com", "STU007"),
    ]
    cur.executemany("""INSERT INTO rsvps
        (event_id, student_name, student_email, student_id)
        VALUES (?, ?, ?, ?)""", sample_rsvps)

    sample_attendance = [
        (event_ids[0], "aarav@example.com", 1),
        (event_ids[0], "meera@example.com", 1),
        (event_ids[1], "riya@example.com", 1),
        (event_ids[1], "kiran@example.com", 0),
        (event_ids[1], "ananya@example.com", 1),
        (event_ids[2], "dev@example.com", 1),
        (event_ids[3], "isha@example.com", 1),
    ]
    cur.executemany("""INSERT INTO attendance(event_id, student_email, attended)
                       VALUES (?, ?, ?)""", sample_attendance)
