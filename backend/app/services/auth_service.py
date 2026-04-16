from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app

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
