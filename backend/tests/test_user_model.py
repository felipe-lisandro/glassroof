"""
test_user_model.py — unit tests for the User model hierarchy.

Covers:
- Password hashing and verification
- to_dict() output for all three model types
- Polymorphic identity values
- Nullable / unique constraints
"""

import pytest
from datetime import date

from app import db
from app.models.user import EnterpriseUser, PersonUser, User


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_person(**kwargs) -> PersonUser:
    defaults = dict(
        name="Alice",
        email="alice@example.com",
        cpf="12345678901",
        last_name="Smith",
        birthday=date(1995, 6, 15),
    )
    defaults.update(kwargs)
    user = PersonUser(**defaults)
    user.set_password("secret123")
    return user


def make_enterprise(**kwargs) -> EnterpriseUser:
    defaults = dict(
        name="Acme Corp",
        email="acme@example.com",
        cnpj="12345678000199",
    )
    defaults.update(kwargs)
    user = EnterpriseUser(**defaults)
    user.set_password("secret123")
    return user


# ---------------------------------------------------------------------------
# Password tests
# ---------------------------------------------------------------------------

class TestPasswordHashing:
    def test_password_is_hashed(self):
        user = make_person()
        assert user.password_hash != "secret123"

    def test_correct_password_passes(self):
        user = make_person()
        assert user.check_password("secret123") is True

    def test_wrong_password_fails(self):
        user = make_person()
        assert user.check_password("wrongpass") is False

    def test_empty_password_fails_against_real_hash(self):
        user = make_person()
        assert user.check_password("") is False


# ---------------------------------------------------------------------------
# Polymorphic identity
# ---------------------------------------------------------------------------

class TestPolymorphicIdentity:
    def test_person_user_type(self, app):
        with app.app_context():
            user = make_person()
            db.session.add(user)
            db.session.commit()
            assert user.type == "person"

    def test_enterprise_user_type(self, app):
        with app.app_context():
            user = make_enterprise()
            db.session.add(user)
            db.session.commit()
            assert user.type == "enterprise"


# ---------------------------------------------------------------------------
# to_dict() tests
# ---------------------------------------------------------------------------

class TestPersonUserToDict:
    def test_contains_base_fields(self, app):
        with app.app_context():
            user = make_person()
            db.session.add(user)
            db.session.commit()
            d = user.to_dict()
            for key in ("id", "name", "email", "register_date", "type"):
                assert key in d

    def test_contains_person_fields(self, app):
        with app.app_context():
            user = make_person()
            db.session.add(user)
            db.session.commit()
            d = user.to_dict()
            assert d["cpf"] == "12345678901"
            assert d["last_name"] == "Smith"
            assert d["birthday"] == "1995-06-15"

    def test_birthday_none_serialises_as_none(self, app):
        with app.app_context():
            user = make_person(birthday=None)
            db.session.add(user)
            db.session.commit()
            assert user.to_dict()["birthday"] is None

    def test_register_date_is_iso_string(self, app):
        with app.app_context():
            user = make_person()
            db.session.add(user)
            db.session.commit()
            reg = user.to_dict()["register_date"]
            # Must be parseable as a date
            date.fromisoformat(reg)

    def test_password_hash_not_in_dict(self, app):
        with app.app_context():
            user = make_person()
            db.session.add(user)
            db.session.commit()
            assert "password_hash" not in user.to_dict()
            assert "password" not in user.to_dict()


class TestEnterpriseUserToDict:
    def test_contains_cnpj(self, app):
        with app.app_context():
            user = make_enterprise()
            db.session.add(user)
            db.session.commit()
            assert user.to_dict()["cnpj"] == "12345678000199"

    def test_type_is_enterprise(self, app):
        with app.app_context():
            user = make_enterprise()
            db.session.add(user)
            db.session.commit()
            assert user.to_dict()["type"] == "enterprise"


# ---------------------------------------------------------------------------
# Unique constraint tests
# ---------------------------------------------------------------------------

class TestUniqueConstraints:
    def test_duplicate_email_raises(self, app):
        with app.app_context():
            u1 = make_person(email="dup@example.com", cpf="11111111111")
            u2 = make_person(email="dup@example.com", cpf="22222222222")
            db.session.add(u1)
            db.session.commit()
            db.session.add(u2)
            with pytest.raises(Exception):
                db.session.commit()

    def test_duplicate_cpf_raises(self, app):
        with app.app_context():
            u1 = make_person(email="a@example.com", cpf="99999999999")
            u2 = make_person(email="b@example.com", cpf="99999999999")
            db.session.add(u1)
            db.session.commit()
            db.session.add(u2)
            with pytest.raises(Exception):
                db.session.commit()

    def test_duplicate_cnpj_raises(self, app):
        with app.app_context():
            u1 = make_enterprise(email="a@corp.com", cnpj="00000000000100")
            u2 = make_enterprise(email="b@corp.com", cnpj="00000000000100")
            db.session.add(u1)
            db.session.commit()
            db.session.add(u2)
            with pytest.raises(Exception):
                db.session.commit()
