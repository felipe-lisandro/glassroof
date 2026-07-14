from app import db
from app.models.avaliation import Avaliation
from app.models.category import Category
from app.services.avaliation_validation import AvaliationValidationFactory
from app.exceptions import BadRequest, NotFound, Forbidden


def _assert_user_never_reviewed_property(property_id: int, user_id: int) -> None:
    already_reviewed = Avaliation.query.filter_by(property_id=property_id, user_id=user_id).first()
    if already_reviewed:
        raise BadRequest("User already reviewed this property")


def create_avaliation(property_id: int, data: dict) -> dict:
    validated = AvaliationValidationFactory.get_validator("create").validate(property_id, data)

    user_obj = validated["user"]
    _assert_user_never_reviewed_property(property_id, user_obj.id)

    avaliation = Avaliation(
        property_id=property_id,
        user_id=user_obj.id,
        category_id=validated["category"].id,
        comment=validated["comment"],
        stars=validated["stars"],
        photos=validated["photos"],
    )

    db.session.add(avaliation)
    db.session.commit()
    return avaliation.to_dict()


def create_avaliations_bulk(property_id: int, data: dict) -> list[dict]:
    validated = AvaliationValidationFactory.get_validator("bulk").validate(property_id, data)

    user_obj = validated["user"]
    _assert_user_never_reviewed_property(property_id, user_obj.id)

    created: list[Avaliation] = []
    for item in validated["avaliations"]:
        avaliation = Avaliation(
            property_id=property_id,
            user_id=user_obj.id,
            category_id=item["category"].id,
            comment=item["comment"],
            stars=item["stars"],
            photos=item["photos"],
        )
        created.append(avaliation)
        db.session.add(avaliation)

    db.session.commit()
    return [item.to_dict() for item in created]


def list_avaliations(property_id: int, stars: int | None = None) -> list[dict]:
    validated = AvaliationValidationFactory.get_validator("list").validate(property_id, stars)

    query = (
        db.session.query(Avaliation, Category.name.label("category_name"))
        .join(Category, Avaliation.category_id == Category.id)
        .filter(Avaliation.property_id == property_id)
    )

    if validated["stars"] is not None:
        query = query.filter(Avaliation.stars == validated["stars"])

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
        raise NotFound("Avaliation not found")

    if avaliation.user_id != user_id:
        raise Forbidden("You can only update your own avaliation")

    validated = AvaliationValidationFactory.get_validator("update").validate(data)

    avaliation.comment = validated["comment"]
    avaliation.stars = validated["stars"]
    if "photos" in validated:
        avaliation.photos = validated["photos"]

    db.session.commit()
    return avaliation.to_dict()


def delete_avaliation(property_id: int, avaliation_id: int, user_id: int) -> None:
    avaliation = db.session.get(Avaliation, avaliation_id)
    if not avaliation or avaliation.property_id != property_id:
        raise NotFound("Avaliation not found")

    if avaliation.user_id != user_id:
        raise Forbidden("You can only delete your own avaliation")

    db.session.delete(avaliation)
    db.session.commit()
