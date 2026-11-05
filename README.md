# Campus Event Calendar & RSVP System

A responsive campus-event management web application inspired by the clean, modular structure of the referenced SongNet repository.

Team:
KP Preetika Setty
Karanam Srujana
K Prashanthi

## Features
- Responsive calendar with month/week/list views
- Upcoming campus event listing
- Event details and RSVP workflow
- Duplicate RSVP prevention
- Attendance recording
- Attendance summary dashboard
- CSV export for attendance and RSVP reports
- SQLite database with automatic initialization and sample data
- Flask REST API
- Pytest API tests

## Security
The current application has no administrator authentication or authorization. Event creation, editing, and deletion endpoints are publicly accessible; hiding their buttons in the interface would not secure them. Before deployment, add server-enforced administrator login and role checks (for example, secure sessions with password hashing and CSRF protection), and protect the event-management API routes with those checks. Public event viewing and RSVP behavior can remain separate.

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Calendar: FullCalendar
- Backend: Python Flask
- Database: SQLite
- Charts: Chart.js
- Testing: Pytest

## Project Structure
```text
Campus-Event-Calendar/
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── routes/
│   │   ├── events.py
│   │   ├── rsvp.py
│   │   └── reports.py
│   └── services/
│       └── csv_export.py
├── data/
│   └── events.csv
├── frontend/
│   ├── index.html
│   ├── calendar.html
│   ├── events.html
│   ├── reports.html
│   ├── css/style.css
│   └── js/
│       ├── calendar.js
│       ├── events.js
│       └── reports.js
├── tests/
│   ├── conftest.py
│   ├── test_events.py
│   ├── test_rsvp.py
│   └── test_reports.py
├── requirements.txt
└── .gitignore
```

## Setup
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python backend/app.py
```

Open `http://127.0.0.1:5000`.

The SQLite database is created automatically as `backend/campus_events.db`.

## API
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/events` | List events |
| GET | `/api/events/<id>` | Event details |
| POST | `/api/events` | Create event |
| PUT | `/api/events/<id>` | Update event |
| DELETE | `/api/events/<id>` | Delete event |
| POST | `/api/events/<id>/rsvp` | RSVP |
| DELETE | `/api/events/<id>/rsvp` | Cancel RSVP |
| GET | `/api/events/<id>/attendance` | Event attendance |
| POST | `/api/events/<id>/attendance` | Record attendance |
| GET | `/api/reports/attendance` | Attendance summary |
| GET | `/api/reports/rsvp` | RSVP summary |
| GET | `/api/reports/attendance/csv` | Download attendance CSV |
| GET | `/api/reports/rsvp/csv` | Download RSVP CSV |

## Testing
```bash
pytest -q
```

## Sample Data
The first run inserts sample campus events and student RSVPs automatically. A CSV copy of the sample events is also provided in `data/events.csv`.

## Academic Note
This is a functional full-stack project suitable for a software engineering / DBMS-style capstone or lab demonstration. Authentication and role-based administration can be added as a future enhancement.
