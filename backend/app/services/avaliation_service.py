from app import db
from app.models.avaliation import Avaliation
from app.models.category import Category
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

    category_id = data.get("category_id")
    if category_id is None:
        raise ValueError("category_id is required")

    try:
        category_id = int(category_id)
    except (TypeError, ValueError) as exc:
        raise ValueError("category_id must be an integer") from exc

    category_obj = db.session.get(Category, category_id)
    if not category_obj:
        raise ValueError("Category not found")

    avaliation = Avaliation(
        property_id=property_id,
        category_id=category_id,
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

    query = (
        db.session.query(Avaliation, Category.name.label("category_name"))
        .join(Category, Avaliation.category_id == Category.id)
        .filter(Avaliation.property_id == property_id)
    )

    if stars is not None:
        try:
            stars_filter = int(stars)
        except (TypeError, ValueError) as exc:
            raise ValueError("stars must be an integer between 0 and 5") from exc

        if not 0 <= stars_filter <= 5:
            raise ValueError("stars must be between 0 and 5")

        query = query.filter(Avaliation.stars == stars_filter)

    rows = query.order_by(Avaliation.created_at.desc()).all()
    result = []
    for avaliation, category_name in rows:
        item = avaliation.to_dict()
        item["category_name"] = category_name
        result.append(item)
    return result
