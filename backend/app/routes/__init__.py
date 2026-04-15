from flask import Blueprint

api_bp = Blueprint("api", __name__)

from app.routes import health_routes  # noqa: E402
