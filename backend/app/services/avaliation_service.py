from app import db
from app.models.avaliation import Avaliation

def create_avaliation(data: dict) -> dict:
    avaliation = Avaliation(
        message=data["message"],
        rate_given=data["rate_given"],
        category_id=data["category_id"]
    )

    db.session.add(avaliation)
    db.session.commit()
    return avaliation.to_dict()


def get_avaliations_from_category(category_id: int) -> list[dict]:
    avaliations = Avaliation.query.filter_by(category_id=category_id).all()
    return [a.to_dict() for a in avaliations]


def get_avaliation_by_id(avaliation_id: int) -> dict | None:
    avaliation = db.session.get(Avaliation, avaliation_id)
    return avaliation.to_dict() if avaliation else None
