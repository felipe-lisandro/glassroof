from datetime import datetime, timezone

from app import db


class ChatRoom(db.Model):
    __tablename__ = "chat_rooms"

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)
    visit_id = db.Column(db.Integer, db.ForeignKey("visits.id"), nullable=False, unique=True)
    person_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    enterprise_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_message_at = db.Column(db.DateTime, nullable=True)

    property = db.relationship("Property", foreign_keys=[property_id], backref="chat_rooms")
    visit = db.relationship("Visit", foreign_keys=[visit_id], backref="chat_room", uselist=False)
    person_user = db.relationship("User", foreign_keys=[person_user_id])
    enterprise_user = db.relationship("User", foreign_keys=[enterprise_user_id])

    def to_dict(self) -> dict:
        latest_message = None
        if getattr(self, "messages", None):
            latest_message = max(self.messages, key=lambda message: message.created_at)

        return {
            "id": self.id,
            "property_id": self.property_id,
            "visit_id": self.visit_id,
            "person_user_id": self.person_user_id,
            "enterprise_user_id": self.enterprise_user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_message_at": self.last_message_at.isoformat() if self.last_message_at else None,
            "property": {
                "id": self.property.id,
                "name": self.property.name,
                "price": self.property.price,
            } if self.property else None,
            "visit": {
                "id": self.visit.id,
                "scheduled_at": self.visit.scheduled_at.isoformat() if self.visit and self.visit.scheduled_at else None,
                "status": self.visit.status,
            } if self.visit else None,
            "participants": {
                "person": self.person_user.to_dict() if self.person_user else None,
                "enterprise": self.enterprise_user.to_dict() if self.enterprise_user else None,
            },
            "latest_message": latest_message.to_dict() if latest_message else None,
        }