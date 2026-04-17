from datetime import date

from app import db


class Avaliation(db.Model):
    __tablename__ = "avaliation"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(240), nullable=False)
    rate_given = db.Column(db.Float, nullable=False)
    sent_day = db.Column(db.Date, default=date.today, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "message": self.message,
            "rate_given": self.rate_given,
            "sent_day": self.sent_day,
        }

