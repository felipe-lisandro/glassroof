"""
test_user_service.py — unit tests for the service layer.

Each function in user_service is tested in isolation.
The in-memory DB from conftest ensures no cross-test pollution.
"""

import pytest
from datetime import date

from app import db
from app.models.user import EnterpriseUser, PersonUser, User
from app.services.user_service import (
    DuplicateError,
    create_enterprise_user,
    create_person_user,
    get_all_users,
    get_user_by_id,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

PERSON_DATA = {
    "name": "Carlos",
    "email": "carlos@example.com",
    "password": "pass1234",
    "cpf": "12345678901",
    "last_name": "Silva",
    "birthday": date(1990, 3, 22),
}

ENTERPRISE_DATA = {
    "name": "Tech Ltda",
    "email": "tech@ltda.com",
    "password": "pass5678",
    "cnpj": "12345678000199",
}


# ---------------------------------------------------------------------------
# create_person_user
# ---------------------------------------------------------------------------

class TestCreatePersonUser:
    def test_creates_and_returns_dict(self, app):
        with app.app_context():
            result = create_person_user(PERSON_DATA)
            assert isinstance(result, dict)
            assert result["email"] == PERSON_DATA["email"]
            assert result["type"] == "person"

    def test_persists_to_database(self, app):
        with app.app_context():
            create_person_user(PERSON_DATA)
            assert PersonUser.query.filter_by(email=PERSON_DATA["email"]).first() is not None

    def test_password_is_hashed_not_plain(self, app):
        with app.app_context():
            create_person_user(PERSON_DATA)
            user = PersonUser.query.filter_by(email=PERSON_DATA["email"]).first()
            assert user.password_hash != PERSON_DATA["password"]
            assert user.check_password(PERSON_DATA["password"]) is True

    def test_duplicate_email_raises_duplicate_error(self, app):
        with app.app_context():
            create_person_user(PERSON_DATA)
            duplicate = {**PERSON_DATA, "cpf": "99999999999"}
            with pytest.raises(DuplicateError, match="Email"):
                create_person_user(duplicate)

    def test_duplicate_cpf_raises_duplicate_error(self, app):
        with app.app_context():
            create_person_user(PERSON_DATA)
            duplicate = {**PERSON_DATA, "email": "other@example.com"}
            with pytest.raises(DuplicateError, match="CPF"):
                create_person_user(duplicate)

    def test_optional_fields_are_stored(self, app):
        with app.app_context():
            result = create_person_user(PERSON_DATA)
            assert result["last_name"] == "Silva"
            assert result["birthday"] == "1990-03-22"

    def test_optional_fields_default_to_none(self, app):
        with app.app_context():
            data = {k: v for k, v in PERSON_DATA.items() if k not in ("last_name", "birthday")}
            result = create_person_user(data)
            assert result["last_name"] is None
            assert result["birthday"] is None


# ---------------------------------------------------------------------------
# create_enterprise_user
# ---------------------------------------------------------------------------

class TestCreateEnterpriseUser:
    def test_creates_and_returns_dict(self, app):
        with app.app_context():
            result = create_enterprise_user(ENTERPRISE_DATA)
            assert result["type"] == "enterprise"
            assert result["name"] == "Tech Ltda"

    def test_cnpj_is_stored(self, app):
        with app.app_context():
            result = create_enterprise_user(ENTERPRISE_DATA)
            assert result["cnpj"] == ENTERPRISE_DATA["cnpj"]

    def test_duplicate_email_raises(self, app):
        with app.app_context():
            create_enterprise_user(ENTERPRISE_DATA)
            dup = {**ENTERPRISE_DATA, "cnpj": "98765432000100"}
            with pytest.raises(DuplicateError, match="Email"):
                create_enterprise_user(dup)

    def test_duplicate_cnpj_raises(self, app):
        with app.app_context():
            create_enterprise_user(ENTERPRISE_DATA)
            dup = {**ENTERPRISE_DATA, "email": "other@corp.com"}
            with pytest.raises(DuplicateError, match="CNPJ"):
                create_enterprise_user(dup)

    def test_password_is_hashed(self, app):
        with app.app_context():
            create_enterprise_user(ENTERPRISE_DATA)
            user = EnterpriseUser.query.filter_by(email=ENTERPRISE_DATA["email"]).first()
            assert user.check_password(ENTERPRISE_DATA["password"]) is True


# ---------------------------------------------------------------------------
# get_all_users
# ---------------------------------------------------------------------------

class TestGetAllUsers:
    def test_returns_empty_list_when_no_users(self, app):
        with app.app_context():
            assert get_all_users() == []

    def test_returns_all_users(self, app):
        with app.app_context():
            create_person_user(PERSON_DATA)
            create_enterprise_user(ENTERPRISE_DATA)
            result = get_all_users()
            assert len(result) == 2

    def test_returns_list_of_dicts(self, app):
        with app.app_context():
            create_person_user(PERSON_DATA)
            result = get_all_users()
            assert all(isinstance(u, dict) for u in result)

    def test_includes_both_user_types(self, app):
        with app.app_context():
            create_person_user(PERSON_DATA)
            create_enterprise_user(ENTERPRISE_DATA)
            types = {u["type"] for u in get_all_users()}
            assert types == {"person", "enterprise"}


# ---------------------------------------------------------------------------
# get_user_by_id
# ---------------------------------------------------------------------------

class TestGetUserById:
    def test_returns_dict_for_existing_user(self, app):
        with app.app_context():
            created = create_person_user(PERSON_DATA)
            result = get_user_by_id(created["id"])
            assert result is not None
            assert result["id"] == created["id"]

    def test_returns_none_for_missing_id(self, app):
        with app.app_context():
            assert get_user_by_id(99999) is None

    def test_returns_correct_user(self, app):
        with app.app_context():
            p = create_person_user(PERSON_DATA)
            e = create_enterprise_user(ENTERPRISE_DATA)
            assert get_user_by_id(p["id"])["email"] == PERSON_DATA["email"]
            assert get_user_by_id(e["id"])["email"] == ENTERPRISE_DATA["email"]
