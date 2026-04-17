from app import db
from app.models.image import Image

def create_image(data: dict) -> dict:
    image = Image(
        URL=data["URL"],
        size_mb=data["size_mb"],
        order=data["order"],
        description=data["description"],
        property_id=data["property_id"]
    )

    db.session.add(image)
    db.session.commit()
    return image.to_dict()


def get_images_from_property(property_id: int) -> list[dict]:
    images = Image.query.filter_by(property_id=property_id).all()
    return [image.to_dict() for image in images]


def get_image_by_id(image_id: int) -> dict | None:
    image = db.session.get(Image, image_id)
    return image.to_dict() if image else None
