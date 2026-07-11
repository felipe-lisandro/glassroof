from app import db
from app.models.avaliation import Avaliation
from app.models.property import Property


def create_avaliation(property_id: int, data: dict) -> dict:
    property_obj = db.session.get(Property, property_id)
    if not property_obj:
        raise ValueError("Property not found")

    comment = (data.get("comment") or "").strip()
    if not comment:
        raise ValueError("comment is required")

    try:
        stars = int(data.get("stars"))
    except (TypeError, ValueError) as exc:
        raise ValueError("stars must be an integer between 0 and 5") from exc

    if not 0 <= stars <= 5:
        raise ValueError("stars must be between 0 and 5")

    photos = data.get("photos")
    if photos is not None and not isinstance(photos, list):
        raise ValueError("photos must be a list of URLs")

    avaliation = Avaliation(
        property_id=property_id,
        comment=comment,
        stars=stars,
        photos=photos,
    )

    db.session.add(avaliation)
    db.session.commit()
    return avaliation.to_dict()


def list_avaliations(property_id: int, stars: int | None = None) -> list[dict]:
    property_obj = db.session.get(Property, property_id)
    if not property_obj:
        raise ValueError("Property not found")

    query = Avaliation.query.filter_by(property_id=property_id)

    if stars is not None:
        try:
            stars_filter = int(stars)
        except (TypeError, ValueError) as exc:
            raise ValueError("stars must be an integer between 0 and 5") from exc

        if not 0 <= stars_filter <= 5:
            raise ValueError("stars must be between 0 and 5")

        query = query.filter_by(stars=stars_filter)

    return [item.to_dict() for item in query.order_by(Avaliation.created_at.desc()).all()]
