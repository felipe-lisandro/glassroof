from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app, request, jsonify
from functools import wraps

from app import db
from app.models.user import User


class InvalidCredentialsError(Exception):
    """Raised when email or password is wrong."""


def authenticate_user(email: str, password: str) -> User:
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        raise InvalidCredentialsError("Email ou senha inválidos")
    return user


def generate_token(user: User) -> str:
    payload = {
        "user_id": user.id,
        "email": user.email,
        "type": user.type,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_token(token: str) -> dict:
    return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])


def get_user_from_token(token: str) -> User | None:
    data = decode_token(token)
    return db.session.get(User, data["user_id"])

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"].split(" ")
            if len(auth_header) == 2:
                token = auth_header[1]

        if not token:
            return jsonify({"error": "Token de autenticação ausente"}), 401

        try:
            current_user = get_user_from_token(token)
            if not current_user:
                return jsonify({"error": "Usuário inválido"}), 401
        except Exception:
            return jsonify({"error": "Token inválido ou expirado"}), 401

        return f(current_user, *args, **kwargs)

    return decorated
