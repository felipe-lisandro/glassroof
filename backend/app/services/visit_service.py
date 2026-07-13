from datetime import datetime

from app import db
from app.models.property import Property
from app.models.user import User
from app.models.visit import Visit


class VisitError(Exception):
    pass


def create_visit(data: dict) -> dict:
    property_obj = db.session.get(Property, data.get("property_id"))
    if not property_obj:
        raise VisitError("Property not found")

    user_obj = db.session.get(User, data.get("user_id"))
    if not user_obj:
        raise VisitError("User not found")

    scheduled_at = data.get("scheduled_at")
    if not scheduled_at:
        raise VisitError("scheduled_at is required")

    if isinstance(scheduled_at, str):
        try:
            scheduled_at = datetime.fromisoformat(scheduled_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise VisitError("scheduled_at must be a valid datetime") from exc

    if not isinstance(scheduled_at, datetime):
        raise VisitError("scheduled_at must be a valid datetime")

    note = data.get("note")
    if note is not None and len(note.strip()) > 500:
        raise VisitError("note must be at most 500 characters")

    visit = Visit(
        property_id=property_obj.id,
        user_id=user_obj.id,
        scheduled_at=scheduled_at,
        status=data.get("status", "pending"),
        note=note.strip() if note else None,
    )

    db.session.add(visit)
    db.session.commit()
    return visit.to_dict()


def list_visits(property_id: int | None = None, user_id: int | None = None) -> list[dict]:
    query = Visit.query

    if property_id is not None:
        query = query.filter_by(property_id=property_id)
    if user_id is not None:
        query = query.filter_by(user_id=user_id)

    return [visit.to_dict() for visit in query.order_by(Visit.scheduled_at.asc()).all()]


def get_visit_by_id(visit_id: int) -> dict | None:
    visit = db.session.get(Visit, visit_id)
    return visit.to_dict() if visit else None


def update_visit_status(visit_id: int, status: str) -> dict | None:
    visit = db.session.get(Visit, visit_id)
    if not visit:
        raise VisitError("Visit not found")

    if status not in {"pending", "confirmed", "cancelled"}:
        raise VisitError("status must be one of pending, confirmed, cancelled")

    visit.status = status
    db.session.commit()
    return visit.to_dict()
