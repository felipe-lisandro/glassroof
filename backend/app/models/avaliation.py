from datetime import datetime, timezone

from app import db


class Avaliation(db.Model):
    __tablename__ = "avaliation"

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    photos = db.Column(db.JSON, nullable=True)

    category = db.relationship("Category", backref="avaliations")
    user = db.relationship("User", backref="avaliations")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "property_id": self.property_id,
            "user_id": self.user_id,
            "user_name": self.user.name if self.user else None,
            "category_id": self.category_id,
            "category_name": self.category.name if self.category else None,
            "comment": self.comment,
            "stars": self.stars,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "photos": self.photos or [],
        }

