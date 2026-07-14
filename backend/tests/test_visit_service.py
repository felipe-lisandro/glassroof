from datetime import datetime, timedelta

import pytest

from app import db
from app.models.property import Property
from app.services.user_service import create_enterprise_user, create_person_user
from app.services.visit_service import (
    VisitError,
    create_visit,
    list_visits,
    list_visits_for_enterprise,
    update_visit_status,
)


def create_property(suffix):
    enterprise = create_enterprise_user(
        {
            "name": f"Empresa {suffix}",
            "email": f"empresa{suffix}@teste.com",
            "password": "pass1234",
            "cnpj": f"{suffix:014d}",
        }
    )
    property_obj = Property(
        name=f"Casa {suffix}",
        description="Casa para teste",
        price=250000,
        enterprise_id=enterprise["id"],
    )
    db.session.add(property_obj)
    db.session.commit()
    return enterprise, property_obj


def create_person(suffix):
    return create_person_user(
        {
            "name": f"Pessoa {suffix}",
            "email": f"pessoa{suffix}@teste.com",
            "password": "pass1234",
            "cpf": f"{suffix:011d}",
        }
    )


class TestCreateVisit:
    def test_creates_pending_future_visit(self, app):
        with app.app_context():
            _, property_obj = create_property(1)
            person = create_person(1)
            result = create_visit(
                {
                    "property_id": property_obj.id,
                    "user_id": person["id"],
                    "scheduled_at": (
                        datetime.now() + timedelta(days=2)
                    ).isoformat(),
                }
            )

            assert result["status"] == "pending"

    def test_rejects_past_date(self, app):
        with app.app_context():
            _, property_obj = create_property(2)
            person = create_person(2)

            with pytest.raises(VisitError, match="past"):
                create_visit(
                    {
                        "property_id": property_obj.id,
                        "user_id": person["id"],
                        "scheduled_at": (
                            datetime.now() - timedelta(days=1)
                        ).isoformat(),
                    }
                )


class TestVisitStatus:
    def test_only_property_owner_can_update_status(self, app):
        with app.app_context():
            enterprise, property_obj = create_property(3)
            other_enterprise, _ = create_property(4)
            person = create_person(3)
            visit = create_visit(
                {
                    "property_id": property_obj.id,
                    "user_id": person["id"],
                    "scheduled_at": (
                        datetime.now() + timedelta(days=2)
                    ).isoformat(),
                }
            )

            with pytest.raises(PermissionError):
                update_visit_status(
                    visit["id"], "confirmed", other_enterprise["id"]
                )

            updated = update_visit_status(
                visit["id"], "confirmed", enterprise["id"]
            )
            assert updated["status"] == "confirmed"


class TestVisitQueries:
    def test_lists_user_and_enterprise_visits(self, app):
        with app.app_context():
            enterprise, property_obj = create_property(5)
            person = create_person(5)
            create_visit(
                {
                    "property_id": property_obj.id,
                    "user_id": person["id"],
                    "scheduled_at": (
                        datetime.now() + timedelta(days=2)
                    ).isoformat(),
                }
            )

            assert len(list_visits(user_id=person["id"])) == 1
            assert len(list_visits_for_enterprise(enterprise["id"])) == 1
