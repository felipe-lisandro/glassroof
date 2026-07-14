from app import db
from app.models.avaliation import Avaliation
from app.models.property import Property
from app.services.property_service import get_all_properties
from app.services.user_service import create_enterprise_user


def make_property(suffix, price=200000):
    enterprise = create_enterprise_user(
        {
            "name": f"Empresa {suffix}",
            "email": f"empresa{suffix}@teste.com",
            "password": "pass1234",
            "cnpj": f"{suffix:014d}",
        }
    )
    property_obj = Property(
        name=f"Imóvel {suffix}",
        description="Imóvel para teste",
        price=price,
        enterprise_id=enterprise["id"],
    )
    db.session.add(property_obj)
    db.session.commit()
    return property_obj


def test_get_all_properties_calculates_average_rating(app):
    with app.app_context():
        property_obj = make_property(1)
        db.session.add_all(
            [
                Avaliation(
                    property_id=property_obj.id,
                    user_id=1,
                    category_id=1,
                    comment="Bom",
                    stars=5,
                ),
                Avaliation(
                    property_id=property_obj.id,
                    user_id=2,
                    category_id=1,
                    comment="Regular",
                    stars=3,
                ),
            ]
        )
        db.session.commit()

        result = get_all_properties()

        assert result[0]["overall_rating"] == 4.0


def test_get_all_properties_marks_unrated_property(app):
    with app.app_context():
        property_obj = make_property(2)

        result = get_all_properties()

        assert result[0]["id"] == property_obj.id
        assert result[0]["overall_rating"] is None
