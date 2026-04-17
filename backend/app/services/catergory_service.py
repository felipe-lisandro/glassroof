from app import db
from app.models.category import Category

def create_category(data: dict) -> dict:
    category = Category(
        name=data["name"],
        description=data["description"],
        overall_rating=data.get("overall_rating"),
        property_id=data["property_id"]
    )

    db.session.add(category)
    db.session.commit()
    return category.to_dict()


def get_categories_from_property(property_id: int) -> list[dict]:
    categories = Category.query.filter_by(property_id=property_id).all()
    return [category.to_dict() for category in categories]


def get_category_by_id(category_id: int) -> dict | None:
    category = db.session.get(Category, category_id)
    return category.to_dict() if category else None