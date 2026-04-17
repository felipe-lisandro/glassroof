from app import db


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    overall_rating = db.Column(db.Float, nullable=True)
    avaliations = db.relationship("Avaliation", backref="category", uselist=True)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "overall_rating": self.overall_rating,
        }


