import math

from app import db
from app.models.avaliation import Avaliation
from app.models.location import Location
from app.models.property import Property
from app.services.location_service import create_location
from app.services.image_service import create_image

def create_property(data: dict) -> dict:
    property = Property(
        name=data["name"],
        description=data["description"],
        price=data["price"],
        overall_rating=data.get("overall_rating"),
        enterprise_id=data["enterprise_id"]
    )

    db.session.add(property)
    db.session.flush() 

    location_data = data["location"]
    location_data["property_id"] = property.id
    create_location(location_data)

    for img_data in data["images"]:
        img_data["property_id"] = property.id
        create_image(img_data)

    db.session.commit()
    return property.to_dict()

def update_property(property_id: int, data: dict) -> dict:
    property = db.session.get(Property, property_id)
    if not property:
        return None

    property.name = data.get("name", property.name)
    property.description = data.get("description", property.description)
    property.price = data.get("price", property.price)

    if "location" in data:
        loc_data = data["location"]
        if property.location:
            for key, value in loc_data.items():
                setattr(property.location, key, value)
        else:
            loc_data["property_id"] = property.id
            create_location(loc_data)

    db.session.commit()
    return property.to_dict()

def get_properties_from_enterprise(enterprise_id: int) -> list[dict]:
    properties = Property.query.filter_by(enterprise_id=enterprise_id).all()
    return [property.to_dict() for property in properties]

def get_all_properties(
    min_price: float | None = None,
    max_price: float | None = None,
    city: str | None = None,
    min_rating: float | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    page: int = 1,
    per_page: int = 9,
) -> dict:
    if page < 1:
        raise ValueError("page must be greater than or equal to 1")
    if per_page < 1 or per_page > 100:
        raise ValueError("per_page must be between 1 and 100")
    if sort_by not in {"id", "price", "rating"}:
        raise ValueError("sort_by must be one of id, price, rating")
    if sort_order not in {"asc", "desc"}:
        raise ValueError("sort_order must be asc or desc")
    if min_price is not None and max_price is not None and min_price > max_price:
        raise ValueError("min_price cannot be greater than max_price")

    ratings = (
        db.session.query(
            Avaliation.property_id,
            db.func.avg(Avaliation.stars).label("average_rating"),
        )
        .group_by(Avaliation.property_id)
        .subquery()
    )
    query = (
        db.session.query(Property, ratings.c.average_rating)
        .outerjoin(ratings, ratings.c.property_id == Property.id)
        .outerjoin(Location, Location.property_id == Property.id)
    )

    if min_price is not None:
        query = query.filter(Property.price >= min_price)
    if max_price is not None:
        query = query.filter(Property.price <= max_price)
    if city:
        query = query.filter(Location.city.ilike(f"%{city.strip()}%"))
    if min_rating is not None:
        query = query.filter(ratings.c.average_rating >= min_rating)

    if sort_by == "price":
        sort_column = Property.price
    elif sort_by == "rating":
        sort_column = db.func.coalesce(ratings.c.average_rating, 0)
    else:
        sort_column = Property.id

    sort_column = sort_column.desc() if sort_order == "desc" else sort_column.asc()
    query = query.order_by(sort_column)
    total = query.count()
    rows = query.offset((page - 1) * per_page).limit(per_page).all()

    result = []
    for property, average_rating in rows:
        data = property.to_dict()
        data["overall_rating"] = (
            round(float(average_rating), 1)
            if average_rating is not None
            else property.overall_rating
        )
        result.append(data)

    return {
        "items": result,
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": math.ceil(total / per_page) if total else 0,
    }

def get_property_by_id(property_id: int) -> dict | None:
    property = db.session.get(Property, property_id)
    return property.to_dict() if property else None
