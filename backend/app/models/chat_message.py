from datetime import datetime, timezone

from app import db


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("chat_rooms.id"), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    read_at = db.Column(db.DateTime, nullable=True)

    room = db.relationship("ChatRoom", backref=db.backref("messages", lazy=True, order_by="ChatMessage.created_at.asc()"))
    sender = db.relationship("User", foreign_keys=[sender_id])

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "room_id": self.room_id,
            "sender_id": self.sender_id,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "sender": self.sender.to_dict() if self.sender else None,
        }