from app import db
from app.models.avaliation import Avaliation
from app.models.category import Category
from app.models.property import Property
from app.models.user import User


def _get_valid_person_user(user_id: int) -> User:
    try:
        user_id = int(user_id)
    except (TypeError, ValueError) as exc:
        raise ValueError("user_id must be an integer") from exc

    user_obj = db.session.get(User, user_id)
    if not user_obj:
        raise ValueError("User not found")
    if user_obj.type != "person":
        raise ValueError("Only person users can create avaliations")
    return user_obj


def _assert_user_never_reviewed_property(property_id: int, user_id: int) -> None:
    already_reviewed = Avaliation.query.filter_by(property_id=property_id, user_id=user_id).first()
    if already_reviewed:
        raise ValueError("User already reviewed this property")


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

    user_id = data.get("user_id")
    if user_id is None:
        raise ValueError("user_id is required")

    user_obj = _get_valid_person_user(user_id)
    _assert_user_never_reviewed_property(property_id, user_obj.id)

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
        user_id=user_id,
        category_id=category_id,
        comment=comment,
        stars=stars,
        photos=photos,
    )

    db.session.add(avaliation)
    db.session.commit()
    return avaliation.to_dict()


def create_avaliations_bulk(property_id: int, data: dict) -> list[dict]:
    property_obj = db.session.get(Property, property_id)
    if not property_obj:
        raise ValueError("Property not found")

    user_id = data.get("user_id")
    if user_id is None:
        raise ValueError("user_id is required")

    user_obj = _get_valid_person_user(user_id)
    _assert_user_never_reviewed_property(property_id, user_obj.id)

    items = data.get("avaliations")
    if not isinstance(items, list) or len(items) == 0:
        raise ValueError("avaliations must be a non-empty list")

    seen_categories = set()
    created: list[Avaliation] = []

    for item in items:
        category_id = item.get("category_id")
        if category_id is None:
            raise ValueError("category_id is required")

        try:
            category_id = int(category_id)
        except (TypeError, ValueError) as exc:
            raise ValueError("category_id must be an integer") from exc

        if category_id in seen_categories:
            raise ValueError("category_id must be unique in avaliations list")
        seen_categories.add(category_id)

        category_obj = db.session.get(Category, category_id)
        if not category_obj:
            raise ValueError("Category not found")

        comment = (item.get("comment") or "").strip()
        if not comment:
            raise ValueError("comment is required")

        try:
            stars = int(item.get("stars"))
        except (TypeError, ValueError) as exc:
            raise ValueError("stars must be an integer between 0 and 5") from exc

        if not 0 <= stars <= 5:
            raise ValueError("stars must be between 0 and 5")

        photos = item.get("photos", [])
        if photos is not None and not isinstance(photos, list):
            raise ValueError("photos must be a list of URLs")

        avaliation = Avaliation(
            property_id=property_id,
            user_id=user_obj.id,
            category_id=category_id,
            comment=comment,
            stars=stars,
            photos=photos,
        )
        created.append(avaliation)
        db.session.add(avaliation)

    db.session.commit()
    return [item.to_dict() for item in created]


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


def update_avaliation(property_id: int, avaliation_id: int, user_id: int, data: dict) -> dict:
    avaliation = db.session.get(Avaliation, avaliation_id)
    if not avaliation or avaliation.property_id != property_id:
        raise ValueError("Avaliation not found")

    if avaliation.user_id != user_id:
        raise PermissionError("You can only update your own avaliation")

    comment = data.get("comment")
    if comment is None or not str(comment).strip():
        raise ValueError("comment is required")

    try:
        stars = int(data.get("stars"))
    except (TypeError, ValueError) as exc:
        raise ValueError("stars must be an integer between 0 and 5") from exc

    if not 0 <= stars <= 5:
        raise ValueError("stars must be between 0 and 5")

    avaliation.comment = str(comment).strip()
    avaliation.stars = stars

    if "photos" in data:
        photos = data.get("photos")
        if photos is not None and not isinstance(photos, list):
            raise ValueError("photos must be a list of URLs")
        avaliation.photos = photos

    db.session.commit()
    return avaliation.to_dict()


def delete_avaliation(property_id: int, avaliation_id: int, user_id: int) -> None:
    avaliation = db.session.get(Avaliation, avaliation_id)
    if not avaliation or avaliation.property_id != property_id:
        raise ValueError("Avaliation not found")

    if avaliation.user_id != user_id:
        raise PermissionError("You can only delete your own avaliation")

    db.session.delete(avaliation)
    db.session.commit()
