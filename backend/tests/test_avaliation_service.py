"""
test_avaliation_service.py — unit tests for the rating service layer.
"""

import pytest

from app import db
from app.models.category import Category
from app.models.property import Property
from app.models.user import EnterpriseUser
from app.services.avaliation_service import create_avaliation, list_avaliations
from app.services.user_service import create_enterprise_user


def create_category_for_test(name: str = "Categoria Teste") -> Category:
    category = Category(name=name, description=f"Descricao de {name}")
    db.session.add(category)
    db.session.commit()
    return category


class TestCreateAvaliation:
    def test_creates_and_returns_dict(self, app):
        with app.app_context():
            category = create_category_for_test("Vizinhanca")
            enterprise = create_enterprise_user(
                {
                    "name": "Empresa Teste",
                    "email": "empresa@teste.com",
                    "password": "pass1234",
                    "cnpj": "12345678000199",
                }
            )
            property_obj = Property(
                name="Casa Teste",
                description="Descrição da casa",
                price=250000.0,
                enterprise_id=enterprise["id"],
            )
            db.session.add(property_obj)
            db.session.commit()

            result = create_avaliation(
                property_obj.id,
                {
                    "category_id": category.id,
                    "comment": "Imóvel excelente",
                    "stars": 5,
                    "photos": ["https://img.com/1.jpg"],
                },
            )

            assert isinstance(result, dict)
            assert result["comment"] == "Imóvel excelente"
            assert result["stars"] == 5
            assert result["property_id"] == property_obj.id
            assert result["category_id"] == category.id
            assert result["category_name"] == "Vizinhanca"
            assert result["photos"] == ["https://img.com/1.jpg"]

    def test_persists_to_database(self, app):
        with app.app_context():
            category = create_category_for_test("Localizacao")
            enterprise = create_enterprise_user(
                {
                    "name": "Empresa Teste",
                    "email": "empresa2@teste.com",
                    "password": "pass1234",
                    "cnpj": "98765432000100",
                }
            )
            property_obj = Property(
                name="Casa Teste 2",
                description="Descrição da casa",
                price=320000.0,
                enterprise_id=enterprise["id"],
            )
            db.session.add(property_obj)
            db.session.commit()

            create_avaliation(
                property_obj.id,
                {"category_id": category.id, "comment": "Muito bom", "stars": 4},
            )

            from app.models.avaliation import Avaliation

            saved = Avaliation.query.filter_by(property_id=property_obj.id).first()
            assert saved is not None
            assert saved.comment == "Muito bom"
            assert saved.stars == 4
            assert saved.category_id == category.id

    def test_raises_for_missing_property(self, app):
        with app.app_context():
            category = create_category_for_test("Infraestrutura")
            with pytest.raises(ValueError, match="Property not found"):
                create_avaliation(99999, {"category_id": category.id, "comment": "ok", "stars": 3})

    def test_raises_when_comment_is_blank(self, app):
        with app.app_context():
            category = create_category_for_test("Preco")
            enterprise = create_enterprise_user(
                {
                    "name": "Empresa Teste",
                    "email": "empresa3@teste.com",
                    "password": "pass1234",
                    "cnpj": "11111111000111",
                }
            )
            property_obj = Property(
                name="Casa Teste 3",
                description="Descrição da casa",
                price=180000.0,
                enterprise_id=enterprise["id"],
            )
            db.session.add(property_obj)
            db.session.commit()

            with pytest.raises(ValueError, match="comment is required"):
                create_avaliation(
                    property_obj.id,
                    {"category_id": category.id, "comment": "   ", "stars": 2},
                )

    def test_raises_for_invalid_stars_range(self, app):
        with app.app_context():
            category = create_category_for_test("Experiencia com locatario")
            enterprise = create_enterprise_user(
                {
                    "name": "Empresa Teste",
                    "email": "empresa4@teste.com",
                    "password": "pass1234",
                    "cnpj": "22222222000122",
                }
            )
            property_obj = Property(
                name="Casa Teste 4",
                description="Descrição da casa",
                price=210000.0,
                enterprise_id=enterprise["id"],
            )
            db.session.add(property_obj)
            db.session.commit()

            with pytest.raises(ValueError, match="stars must be between 0 and 5"):
                create_avaliation(
                    property_obj.id,
                    {"category_id": category.id, "comment": "ok", "stars": 6},
                )


class TestListAvaliations:
    def test_returns_empty_list_when_no_ratings(self, app):
        with app.app_context():
            enterprise = create_enterprise_user(
                {
                    "name": "Empresa Teste",
                    "email": "empresa5@teste.com",
                    "password": "pass1234",
                    "cnpj": "33333333000133",
                }
            )
            property_obj = Property(
                name="Casa Teste 5",
                description="Descrição da casa",
                price=260000.0,
                enterprise_id=enterprise["id"],
            )
            db.session.add(property_obj)
            db.session.commit()

            assert list_avaliations(property_obj.id) == []

    def test_filters_by_stars(self, app):
        with app.app_context():
            category = create_category_for_test("Categoria filtro")
            enterprise = create_enterprise_user(
                {
                    "name": "Empresa Teste",
                    "email": "empresa6@teste.com",
                    "password": "pass1234",
                    "cnpj": "44444444000144",
                }
            )
            property_obj = Property(
                name="Casa Teste 6",
                description="Descrição da casa",
                price=290000.0,
                enterprise_id=enterprise["id"],
            )
            db.session.add(property_obj)
            db.session.commit()

            create_avaliation(
                property_obj.id,
                {"category_id": category.id, "comment": "Bom", "stars": 4},
            )
            create_avaliation(
                property_obj.id,
                {"category_id": category.id, "comment": "Ruim", "stars": 2},
            )

            result = list_avaliations(property_obj.id, stars=4)

            assert len(result) == 1
            assert result[0]["stars"] == 4
            assert result[0]["comment"] == "Bom"
            assert result[0]["category_name"] == "Categoria filtro"

    def test_raises_for_missing_property_when_listing(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="Property not found"):
                list_avaliations(99999)

    def test_raises_for_invalid_stars_filter(self, app):
        with app.app_context():
            enterprise = create_enterprise_user(
                {
                    "name": "Empresa Teste",
                    "email": "empresa7@teste.com",
                    "password": "pass1234",
                    "cnpj": "55555555000155",
                }
            )
            property_obj = Property(
                name="Casa Teste 7",
                description="Descrição da casa",
                price=310000.0,
                enterprise_id=enterprise["id"],
            )
            db.session.add(property_obj)
            db.session.commit()

            with pytest.raises(ValueError, match="stars must be between 0 and 5"):
                list_avaliations(property_obj.id, stars=7)
