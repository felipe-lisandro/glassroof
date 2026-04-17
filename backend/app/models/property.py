from datetime import date

from app import db


class Property(db.Model):
    __tablename__ = "property"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300), unique=False, nullable=False)
    register_date = db.Column(db.Date, default=date.today, nullable=False)
    price = db.Column(db.Float, nullable=False)
    overall_rating = db.Column(db.Float, nullable=True)

    location = db.relationship("Location", backref="property", uselist=False)
    images = db.relationship("Image", backref="property", uselist=True)
    categories = db.relationship("Category", backref="property", uselist=True)

    enterprise_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "register_date": self.register_date.isoformat(),
            "price": self.price,
            "overall_rating": self.overall_rating,
            "enterprise_id": self.enterprise_id,
            "location": self.location.to_dict() if self.location else None,
            "images": [image.to_dict() for image in self.images],
            "categories": [category.to_dict() for category in self.categories],
        }


