from app import db
from app.models.category import Category


def create_category(data: dict) -> dict:
    category = Category(
        name=data["name"],
        description=data["description"]
    )

    db.session.add(category)
    db.session.commit()
    return category.to_dict()

def get_category_by_id(category_id: int) -> dict | None:
    category = db.session.get(Category, category_id)
    return category.to_dict() if category else None


def list_categories() -> list[dict]:
    categories = Category.query.order_by(Category.name.asc()).all()
    return [category.to_dict() for category in categories]