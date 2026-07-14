from app import db


class Image(db.Model):
    __tablename__ = "image"

    id = db.Column(db.Integer, primary_key=True)
    URL = db.Column(db.String(300), nullable=False)
    size_mb = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "URL": self.URL,
            "size_mb": self.size_mb,
            "order": self.order,
            "description": self.description,
        }


