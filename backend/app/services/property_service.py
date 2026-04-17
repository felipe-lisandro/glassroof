from app import db
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

def get_all_properties() -> list[dict]:
    properties = Property.query.all()
    return [property.to_dict() for property in properties]

def get_property_by_id(property_id: int) -> dict | None:
    property = db.session.get(Property, property_id)
    return property.to_dict() if property else None
