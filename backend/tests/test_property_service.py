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

        assert result["items"][0]["overall_rating"] == 4.0


def test_get_all_properties_marks_unrated_property(app):
    with app.app_context():
        property_obj = make_property(2)

        result = get_all_properties()

        assert result["items"][0]["id"] == property_obj.id
        assert result["items"][0]["overall_rating"] is None


def test_get_all_properties_filters_sorts_and_paginates(app):
    with app.app_context():
        make_property(3, price=100000)
        make_property(4, price=300000)
        make_property(5, price=200000)

        result = get_all_properties(
            min_price=150000,
            max_price=300000,
            sort_by="price",
            sort_order="desc",
            page=1,
            per_page=1,
        )

        assert result["total"] == 2
        assert result["pages"] == 2
        assert result["items"][0]["price"] == 300000
