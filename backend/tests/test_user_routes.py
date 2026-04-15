"""
test_user_routes.py — integration tests for /users endpoints.

Exercises the full request → route → service → DB → response pipeline
using Flask's built-in test client.
"""

import json
import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PERSON_PAYLOAD = {
    "name": "Ana",
    "email": "ana@example.com",
    "password": "pass1234",
    "cpf": "12345678901",
    "last_name": "Costa",
    "birthday": "1992-07-10",
}

ENTERPRISE_PAYLOAD = {
    "name": "Construtora ABC",
    "email": "abc@construtora.com",
    "password": "pass5678",
    "cnpj": "12345678000199",
}


def post_json(client, url, data):
    return client.post(url, data=json.dumps(data), content_type="application/json")


# ---------------------------------------------------------------------------
# POST /users/person
# ---------------------------------------------------------------------------

class TestRegisterPerson:
    def test_valid_payload_returns_201(self, client):
        res = post_json(client, "/users/person", PERSON_PAYLOAD)
        assert res.status_code == 201

    def test_response_contains_user_data(self, client):
        res = post_json(client, "/users/person", PERSON_PAYLOAD)
        body = res.get_json()
        assert body["email"] == PERSON_PAYLOAD["email"]
        assert body["type"] == "person"
        assert "id" in body

    def test_password_not_in_response(self, client):
        res = post_json(client, "/users/person", PERSON_PAYLOAD)
        body = res.get_json()
        assert "password" not in body
        assert "password_hash" not in body

    def test_missing_required_field_returns_400(self, client):
        bad = {k: v for k, v in PERSON_PAYLOAD.items() if k != "cpf"}
        res = post_json(client, "/users/person", bad)
        assert res.status_code == 400
        assert "errors" in res.get_json()

    def test_invalid_email_returns_400(self, client):
        bad = {**PERSON_PAYLOAD, "email": "not-an-email"}
        res = post_json(client, "/users/person", bad)
        assert res.status_code == 400

    def test_short_password_returns_400(self, client):
        bad = {**PERSON_PAYLOAD, "password": "123"}
        res = post_json(client, "/users/person", bad)
        assert res.status_code == 400

    def test_cpf_wrong_length_returns_400(self, client):
        bad = {**PERSON_PAYLOAD, "cpf": "123"}
        res = post_json(client, "/users/person", bad)
        assert res.status_code == 400

    def test_duplicate_email_returns_409(self, client):
        post_json(client, "/users/person", PERSON_PAYLOAD)
        dup = {**PERSON_PAYLOAD, "cpf": "99999999999"}
        res = post_json(client, "/users/person", dup)
        assert res.status_code == 409

    def test_duplicate_cpf_returns_409(self, client):
        post_json(client, "/users/person", PERSON_PAYLOAD)
        dup = {**PERSON_PAYLOAD, "email": "other@example.com"}
        res = post_json(client, "/users/person", dup)
        assert res.status_code == 409

    def test_optional_fields_can_be_omitted(self, client):
        minimal = {k: v for k, v in PERSON_PAYLOAD.items()
                   if k not in ("last_name", "birthday")}
        minimal["cpf"] = "00000000001"
        minimal["email"] = "minimal@example.com"
        res = post_json(client, "/users/person", minimal)
        assert res.status_code == 201


# ---------------------------------------------------------------------------
# POST /users/enterprise
# ---------------------------------------------------------------------------

class TestRegisterEnterprise:
    def test_valid_payload_returns_201(self, client):
        res = post_json(client, "/users/enterprise", ENTERPRISE_PAYLOAD)
        assert res.status_code == 201

    def test_response_type_is_enterprise(self, client):
        res = post_json(client, "/users/enterprise", ENTERPRISE_PAYLOAD)
        assert res.get_json()["type"] == "enterprise"

    def test_cnpj_in_response(self, client):
        res = post_json(client, "/users/enterprise", ENTERPRISE_PAYLOAD)
        assert res.get_json()["cnpj"] == ENTERPRISE_PAYLOAD["cnpj"]

    def test_missing_cnpj_returns_400(self, client):
        bad = {k: v for k, v in ENTERPRISE_PAYLOAD.items() if k != "cnpj"}
        res = post_json(client, "/users/enterprise", bad)
        assert res.status_code == 400

    def test_cnpj_wrong_length_returns_400(self, client):
        bad = {**ENTERPRISE_PAYLOAD, "cnpj": "123"}
        res = post_json(client, "/users/enterprise", bad)
        assert res.status_code == 400

    def test_duplicate_email_returns_409(self, client):
        post_json(client, "/users/enterprise", ENTERPRISE_PAYLOAD)
        dup = {**ENTERPRISE_PAYLOAD, "cnpj": "98765432000100"}
        res = post_json(client, "/users/enterprise", dup)
        assert res.status_code == 409

    def test_duplicate_cnpj_returns_409(self, client):
        post_json(client, "/users/enterprise", ENTERPRISE_PAYLOAD)
        dup = {**ENTERPRISE_PAYLOAD, "email": "other@corp.com"}
        res = post_json(client, "/users/enterprise", dup)
        assert res.status_code == 409


# ---------------------------------------------------------------------------
# GET /users
# ---------------------------------------------------------------------------

class TestListUsers:
    def test_returns_200_with_empty_list(self, client):
        res = client.get("/users")
        assert res.status_code == 200
        assert res.get_json() == []

    def test_returns_created_users(self, client):
        post_json(client, "/users/person", PERSON_PAYLOAD)
        post_json(client, "/users/enterprise", ENTERPRISE_PAYLOAD)
        res = client.get("/users")
        assert res.status_code == 200
        assert len(res.get_json()) == 2

    def test_response_is_list(self, client):
        res = client.get("/users")
        assert isinstance(res.get_json(), list)


# ---------------------------------------------------------------------------
# GET /users/<id>
# ---------------------------------------------------------------------------

class TestGetUser:
    def test_existing_user_returns_200(self, client):
        created = post_json(client, "/users/person", PERSON_PAYLOAD).get_json()
        res = client.get(f"/users/{created['id']}")
        assert res.status_code == 200

    def test_response_matches_created_user(self, client):
        created = post_json(client, "/users/person", PERSON_PAYLOAD).get_json()
        res = client.get(f"/users/{created['id']}")
        assert res.get_json()["email"] == PERSON_PAYLOAD["email"]

    def test_nonexistent_id_returns_404(self, client):
        res = client.get("/users/99999")
        assert res.status_code == 404

    def test_404_response_has_error_key(self, client):
        res = client.get("/users/99999")
        assert "error" in res.get_json()
