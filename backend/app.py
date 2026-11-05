from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from pathlib import Path
from .database import DB_PATH, init_db
from .routes.events import events_bp
from .routes.rsvp import rsvp_bp
from .routes.reports import reports_bp

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

def create_app(test_db=None):
    app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
    app.config["DATABASE"] = test_db or DB_PATH
    CORS(app)
    init_db(test_db, seed=(test_db is None))

    app.register_blueprint(events_bp)
    app.register_blueprint(rsvp_bp)
    app.register_blueprint(reports_bp)

    @app.get("/")
    def index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.errorhandler(404)
    def not_found(error):
        if not str(error).startswith("/api/"):
            return send_from_directory(FRONTEND_DIR, "index.html")
        return jsonify({"error":"Not found"}), 404

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
