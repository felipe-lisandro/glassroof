"""
test_avaliation_routes.py — integration tests for the rating endpoints.
"""

import json


def create_property_for_test(app, name, price=250000.0):
    with app.app_context():
        from app import db
        from app.models.property import Property
        from app.services.user_service import create_enterprise_user

        enterprise = create_enterprise_user(
            {
                "name": f"Empresa {name}",
                "email": f"{name.lower().replace(' ', '_')}@teste.com",
                "password": "pass1234",
                "cnpj": "12345678000199",
            }
        )
        property_obj = Property(
            name=name,
            description="Descrição da casa",
            price=price,
            enterprise_id=enterprise["id"],
        )
        db.session.add(property_obj)
        db.session.commit()
        return property_obj.id


class TestCreateAvaliationRoute:
    def test_valid_payload_returns_201(self, client, app):
        property_id = create_property_for_test(app, "Casa para avaliar", 240000.0)
        payload = {"comment": "Excelente imóvel", "stars": 5, "photos": ["https://img.com/1.jpg"]}

        res = client.post(
            f"/properties/{property_id}/avaliations",
            data=json.dumps(payload),
            content_type="application/json",
        )

        assert res.status_code == 201
        body = res.get_json()
        assert body["comment"] == payload["comment"]
        assert body["stars"] == payload["stars"]
        assert body["property_id"] == property_id

    def test_missing_comment_returns_400(self, client):
        payload = {"stars": 4}
        res = client.post(
            "/properties/99999/avaliations",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert res.status_code == 400

    def test_invalid_stars_returns_400(self, client):
        payload = {"comment": "ok", "stars": 6}
        res = client.post(
            "/properties/99999/avaliations",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert res.status_code == 400

    def test_unknown_property_returns_404(self, client):
        payload = {"comment": "ok", "stars": 3}
        res = client.post(
            "/properties/99999/avaliations",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert res.status_code == 404


class TestListAvaliationRoute:
    def test_returns_list_for_property(self, client, app):
        property_id = create_property_for_test(app, "Casa para listar", 260000.0)
        client.post(
            f"/properties/{property_id}/avaliations",
            data=json.dumps({"comment": "Bom", "stars": 4}),
            content_type="application/json",
        )
        client.post(
            f"/properties/{property_id}/avaliations",
            data=json.dumps({"comment": "Ruim", "stars": 2}),
            content_type="application/json",
        )

        res = client.get(f"/properties/{property_id}/avaliations")
        assert res.status_code == 200
        body = res.get_json()
        assert isinstance(body, list)
        assert len(body) == 2

    def test_filters_by_stars_query_param(self, client, app):
        property_id = create_property_for_test(app, "Casa para filtrar", 190000.0)
        client.post(
            f"/properties/{property_id}/avaliations",
            data=json.dumps({"comment": "Ótimo", "stars": 5}),
            content_type="application/json",
        )
        client.post(
            f"/properties/{property_id}/avaliations",
            data=json.dumps({"comment": "Médio", "stars": 3}),
            content_type="application/json",
        )

        res = client.get(f"/properties/{property_id}/avaliations?stars=5")
        assert res.status_code == 200
        body = res.get_json()
        assert len(body) == 1
        assert body[0]["stars"] == 5

    def test_unknown_property_returns_404_when_listing(self, client):
        res = client.get("/properties/99999/avaliations")
        assert res.status_code == 404
