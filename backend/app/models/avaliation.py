from datetime import datetime, timezone

from app import db


class Avaliation(db.Model):
    __tablename__ = "avaliation"

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    photos = db.Column(db.JSON, nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "property_id": self.property_id,
            "comment": self.comment,
            "stars": self.stars,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "photos": self.photos or [],
        }

