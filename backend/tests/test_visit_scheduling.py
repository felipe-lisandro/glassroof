import json
from datetime import datetime, timedelta, timezone

import pytest

from app import db
from app.models.user import PersonUser, EnterpriseUser
from app.models.property import Property
from app.models.visit import Visit


def _create_person(app, email="person@example.com"):
    with app.app_context():
        user = PersonUser(name="Person", email=email, type="person")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        return user.id


def _create_enterprise(app, email="enterprise@example.com"):
    with app.app_context():
        ent = EnterpriseUser(name="Enterprise", email=email, type="enterprise")
        ent.set_password("password")
        db.session.add(ent)
        db.session.commit()
        return ent.id


def _create_property(app, enterprise_id, name="Imovel Test"):
    with app.app_context():
        prop = Property(name=name, description="desc", price=100.0, enterprise_id=enterprise_id)
        db.session.add(prop)
        db.session.commit()
        return prop.id


def _create_visit_payload(prop_id, user_id, scheduled_at=None, note=None):
    if scheduled_at is None:
        scheduled_at = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    payload = {
        "property_id": prop_id,
        "user_id": user_id,
        "scheduled_at": scheduled_at,
    }
    if note is not None:
        payload["note"] = note
    return payload


def test_create_visit_note_length_bva(client, app):
    """
    Boundary value + equivalence tests for `note` length:
    lengths: 0, 1, 500 -> should succeed; 501 -> should fail (400).
    """
    person = _create_person(app, "p1@example.com")
    ent = _create_enterprise(app, "e1@example.com")
    prop = _create_property(app, ent)

    cases = [(0, True), (1, True), (500, True), (501, False)]
    for length, expect_ok in cases:
        note = "" if length == 0 else "a" * length
        payload = _create_visit_payload(prop, person, note=note)
        res = client.post("/visits", data=json.dumps(payload), content_type="application/json")
        if expect_ok:
            assert res.status_code == 201, f"expected 201 for length {length}, got {res.status_code} - {res.data}"
        else:
            assert res.status_code == 400, f"expected 400 for length {length}, got {res.status_code} - {res.data}"


def test_create_visit_invalid_scheduled_at_format(client, app):
    """Invalid datetime format should be rejected by the route/schema (400)."""
    person = _create_person(app, "p2@example.com")
    ent = _create_enterprise(app, "e2@example.com")
    prop = _create_property(app, ent)

    payload = _create_visit_payload(prop, person, scheduled_at="not-a-date")
    res = client.post("/visits", data=json.dumps(payload), content_type="application/json")
    assert res.status_code == 400


def test_update_visit_status_decision_table(client, app):
    """
    Decision table style coverage for `PATCH /visits/<id>/status`:
    - visit exists + valid status -> 200
    - visit exists + invalid status -> 400
    - visit does not exist -> 404
    """
    person = _create_person(app, "p3@example.com")
    ent = _create_enterprise(app, "e3@example.com")
    prop = _create_property(app, ent)

    # create a visit
    payload = _create_visit_payload(prop, person)
    res = client.post("/visits", data=json.dumps(payload), content_type="application/json")
    assert res.status_code == 201
    visit = res.get_json()
    vid = visit["id"]

    # valid status change
    res_ok = client.patch(f"/visits/{vid}/status", data=json.dumps({"status": "confirmed"}), content_type="application/json")
    assert res_ok.status_code == 200
    assert res_ok.get_json().get("status") == "confirmed"

    # invalid status
    res_bad = client.patch(f"/visits/{vid}/status", data=json.dumps({"status": "invalid"}), content_type="application/json")
    assert res_bad.status_code == 400

    # non-existent visit
    res_missing = client.patch(f"/visits/99999/status", data=json.dumps({"status": "confirmed"}), content_type="application/json")
    assert res_missing.status_code == 404


def test_list_visits_pairwise_filters(client, app):
    """
    Pairwise coverage for filters on `GET /visits` using `property_id` and `user_id` combinations.
    """
    p1 = _create_person(app, "p4@example.com")
    p2 = _create_person(app, "p5@example.com")
    ent = _create_enterprise(app, "e4@example.com")
    prop1 = _create_property(app, ent, name="P1")
    prop2 = _create_property(app, ent, name="P2")

    # create visits: (prop1, p1), (prop1, p2), (prop2, p1)
    payloads = [
        _create_visit_payload(prop1, p1),
        _create_visit_payload(prop1, p2),
        _create_visit_payload(prop2, p1),
    ]
    for payload in payloads:
        r = client.post("/visits", data=json.dumps(payload), content_type="application/json")
        assert r.status_code == 201

    # no filters -> 3
    r_all = client.get("/visits")
    assert r_all.status_code == 200
    assert isinstance(r_all.get_json(), list) and len(r_all.get_json()) == 3

    # filter by property_id (prop1) -> 2
    r_prop = client.get(f"/visits?property_id={prop1}")
    assert r_prop.status_code == 200
    assert len(r_prop.get_json()) == 2

    # filter by user_id (p1) -> 2
    r_user = client.get(f"/visits?user_id={p1}")
    assert r_user.status_code == 200
    assert len(r_user.get_json()) == 2

    # filter by both property_id=prop1 & user_id=p1 -> 1
    r_both = client.get(f"/visits?property_id={prop1}&user_id={p1}")
    assert r_both.status_code == 200
    assert len(r_both.get_json()) == 1


def test_scheduled_at_iso_z_and_offset_acceptance(client, app):
    """Ensure ISO Z timestamps and timezone offsets are parsed and accepted."""
    person = _create_person(app, "pz@example.com")
    ent = _create_enterprise(app, "ez@example.com")
    prop = _create_property(app, ent)

    # Zulu / UTC suffix
    future = (datetime.now(timezone.utc) + timedelta(days=2)).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    payload_z = _create_visit_payload(prop, person, scheduled_at=future)
    rz = client.post("/visits", data=json.dumps(payload_z), content_type="application/json")
    assert rz.status_code == 201

    # timezone offset with fractional seconds
    future2 = (datetime.now(timezone.utc) + timedelta(days=3)).astimezone(timezone(timedelta(hours=2))).isoformat(timespec='milliseconds')
    payload_off = _create_visit_payload(prop, person, scheduled_at=future2)
    ro = client.post("/visits", data=json.dumps(payload_off), content_type="application/json")
    assert ro.status_code == 201


def test_note_trimming_and_whitespace_behavior(client, app):
    """Notes should be trimmed; whitespace-only notes become empty string per current behavior."""
    person = _create_person(app, "nt@example.com")
    ent = _create_enterprise(app, "nte@example.com")
    prop = _create_property(app, ent)

    # trimmed note
    payload = _create_visit_payload(prop, person, note="   hello world  ")
    r = client.post("/visits", data=json.dumps(payload), content_type="application/json")
    assert r.status_code == 201
    visit = r.get_json()
    assert visit.get("note") == "hello world"

    # whitespace-only note -> stored as empty string ("")
    payload2 = _create_visit_payload(prop, person, note="    ")
    r2 = client.post("/visits", data=json.dumps(payload2), content_type="application/json")
    assert r2.status_code == 201
    visit2 = r2.get_json()
    assert visit2.get("note") == ""
