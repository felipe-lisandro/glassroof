from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__)


@api_bp.route("/health")
def health_check():
    from app import db

    try:
        db.session.execute(db.text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return jsonify({"status": "ok", "database": db_status})
