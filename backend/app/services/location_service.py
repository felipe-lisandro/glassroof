from app import db
from app.models.location import Location

def create_location(data: dict) -> dict:
    location = Location(
        street=data["street"],
        number=data["number"],
        CEP=data["CEP"],
        complement=data.get("complement"),
        city=data["city"],
        state=data["state"],
        country=data["country"],
        property_id=data["property_id"]
    )

    db.session.add(location)
    db.session.commit()
    return location.to_dict()


def get_location_from_property(property_id: int) -> list[dict]:
    location = Location.query.filter_by(property_id=property_id).first()
    return location.to_dict() if location else None


def get_location_by_id(location_id: int) -> dict | None:
    location = db.session.get(Location, location_id)
    return location.to_dict() if location else None
