import json
from datetime import datetime, timedelta

from app import socketio
from app.models.property import Property
from app.models.user import EnterpriseUser, PersonUser
from app.models.visit import Visit
from app import db


def post_json(client, url, data, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return client.post(url, data=json.dumps(data), headers=headers)


def get_json(client, url, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return client.get(url, headers=headers)


def create_user_fixtures(app):
    with app.app_context():
        enterprise = EnterpriseUser(
            name="Imobiliaria Teste",
            email="corp@example.com",
            cnpj="12345678000199",
        )
        enterprise.set_password("password123")

        person = PersonUser(
            name="Maria",
            email="maria@example.com",
            cpf="12345678901",
        )
        person.set_password("password123")

        db.session.add_all([enterprise, person])
        db.session.flush()

        property_obj = Property(
            name="Apartamento Centro",
            description="Apartamento amplo",
            price=250000,
            enterprise_id=enterprise.id,
        )
        db.session.add(property_obj)
        db.session.flush()

        visit = Visit(
            property_id=property_obj.id,
            user_id=person.id,
            scheduled_at=datetime.utcnow() + timedelta(days=1),
            status="confirmed",
        )
        db.session.add(visit)
        db.session.commit()

        return {
            "enterprise": enterprise.id,
            "person": person.id,
            "property": property_obj.id,
            "visit": visit.id,
        }


def login(client, email, password):
    response = post_json(client, "/users/login", {"email": email, "password": password})
    assert response.status_code == 200
    return response.get_json()["token"]


class TestChatRoutes:
    def test_person_with_visit_can_create_room(self, client, app):
        ids = create_user_fixtures(app)
        token = login(client, "maria@example.com", "password123")

        response = post_json(client, "/chats", {"property_id": ids["property"]}, token)

        assert response.status_code == 201
        body = response.get_json()
        assert body["property_id"] == ids["property"]
        assert body["visit_id"] == ids["visit"]
        assert body["person_user_id"] == ids["person"]
        assert body["enterprise_user_id"] == ids["enterprise"]

    def test_both_participants_can_list_created_chat(self, client, app):
        ids = create_user_fixtures(app)
        person_token = login(client, "maria@example.com", "password123")
        enterprise_token = login(client, "corp@example.com", "password123")

        create_response = post_json(client, "/chats", {"property_id": ids["property"]}, person_token)
        room_id = create_response.get_json()["id"]

        person_list_response = get_json(client, "/chats", person_token)
        enterprise_list_response = get_json(client, "/chats", enterprise_token)

        assert person_list_response.status_code == 200
        assert enterprise_list_response.status_code == 200
        assert person_list_response.get_json()[0]["id"] == room_id
        assert enterprise_list_response.get_json()[0]["id"] == room_id

    def test_unread_count_is_persisted_and_cleared_when_room_is_read(self, client, app):
        ids = create_user_fixtures(app)
        person_token = login(client, "maria@example.com", "password123")
        enterprise_token = login(client, "corp@example.com", "password123")

        room_response = post_json(client, "/chats", {"property_id": ids["property"]}, person_token)
        room_id = room_response.get_json()["id"]

        message_response = post_json(
            client,
            f"/chats/{room_id}/messages",
            {"content": "Mensagem nova"},
            person_token,
        )
        assert message_response.status_code == 201

        unread_response = get_json(client, "/chats/unread-count", enterprise_token)
        room_list_response = get_json(client, "/chats", enterprise_token)

        assert unread_response.status_code == 200
        assert unread_response.get_json()["unread_count"] == 1
        assert room_list_response.get_json()[0]["unread_count"] == 1

        mark_read_response = post_json(client, f"/chats/{room_id}/read", {}, enterprise_token)
        assert mark_read_response.status_code == 200
        assert mark_read_response.get_json()["marked_count"] == 1
        assert mark_read_response.get_json()["unread_count"] == 0

        unread_after_response = get_json(client, "/chats/unread-count", enterprise_token)
        room_list_after_response = get_json(client, "/chats", enterprise_token)

        assert unread_after_response.get_json()["unread_count"] == 0
        assert room_list_after_response.get_json()[0]["unread_count"] == 0

    def test_person_without_visit_cannot_create_room(self, client, app):
        property_id = None
        with app.app_context():
            enterprise = EnterpriseUser(
                name="Imobiliaria Teste",
                email="corp2@example.com",
                cnpj="99945678000199",
            )
            enterprise.set_password("password123")
            person = PersonUser(
                name="Joao",
                email="joao@example.com",
                cpf="99945678901",
            )
            person.set_password("password123")
            db.session.add_all([enterprise, person])
            db.session.flush()
            property_obj = Property(
                name="Casa Praia",
                description="Casa espaçosa",
                price=700000,
                enterprise_id=enterprise.id,
            )
            db.session.add(property_obj)
            db.session.commit()
            property_id = property_obj.id

        token = login(client, "joao@example.com", "password123")
        response = post_json(client, "/chats", {"property_id": property_id}, token)

        assert response.status_code == 403
        assert "visita marcada" in response.get_json()["error"]

    def test_participants_can_exchange_messages_over_socket(self, client, app):
        ids = create_user_fixtures(app)
        person_token = login(client, "maria@example.com", "password123")
        enterprise_token = login(client, "corp@example.com", "password123")

        room_response = post_json(client, "/chats", {"property_id": ids["property"]}, person_token)
        room_id = room_response.get_json()["id"]

        person_socket = socketio.test_client(app, flask_test_client=client, auth={"token": person_token})
        enterprise_socket = socketio.test_client(app, flask_test_client=client, auth={"token": enterprise_token})

        assert person_socket.is_connected()
        assert enterprise_socket.is_connected()

        person_socket.emit("join_chat", {"token": person_token, "room_id": room_id})
        enterprise_socket.emit("join_chat", {"token": enterprise_token, "room_id": room_id})

        person_socket.get_received()
        enterprise_socket.get_received()

        person_socket.emit(
            "send_message",
            {"token": person_token, "room_id": room_id, "content": "Olá, posso tirar uma dúvida?"},
        )

        received_by_enterprise = enterprise_socket.get_received()
        message_events = [event for event in received_by_enterprise if event["name"] == "message_created"]

        assert len(message_events) == 1
        assert message_events[0]["args"][0]["content"] == "Olá, posso tirar uma dúvida?"

        history_response = get_json(client, f"/chats/{room_id}/messages", enterprise_token)
        assert history_response.status_code == 200
        assert history_response.get_json()[0]["content"] == "Olá, posso tirar uma dúvida?"

        person_socket.disconnect()
        enterprise_socket.disconnect()