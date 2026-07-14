from app import db


class Location(db.Model):
    __tablename__ = "location"

    street = db.Column(db.String(120), primary_key=True)
    number = db.Column(db.Integer, primary_key=True)
    CEP = db.Column(db.String(9), nullable=False)
    complement = db.Column(db.String(300), nullable=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)

    def to_dict(self) -> dict:
        return {
            "street": self.street,
            "number": self.number,
            "CEP": self.CEP,
            "complement": self.complement,
            "city": self.city,
            "state": self.state,
            "country": self.country,
        }


