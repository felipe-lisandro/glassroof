from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import case, or_

from app import db
from app.models.chat_message import ChatMessage
from app.models.chat_room import ChatRoom
from app.models.property import Property
from app.models.user import User
from app.models.visit import Visit


VALID_CHAT_VISIT_STATUSES = {"pending", "confirmed"}


class ChatError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


def get_room_channel(room_id: int) -> str:
    return f"chat_room_{room_id}"


def get_user_channel(user_id: int) -> str:
    return f"chat_user_{user_id}"


def _ensure_room_participant(room: ChatRoom, user: User) -> None:
    if user.id not in {room.person_user_id, room.enterprise_user_id}:
        raise ChatError("Usuário não autorizado para esta sala", 403)


def _get_room_entity(room_id: int) -> ChatRoom:
    room = db.session.get(ChatRoom, room_id)
    if not room:
        raise ChatError("Sala de chat não encontrada", 404)
    return room


def _get_other_participant_id(room: ChatRoom, user: User) -> int:
    return room.enterprise_user_id if room.person_user_id == user.id else room.person_user_id


def count_unread_messages_for_room(room: ChatRoom, user: User) -> int:
    return (
        ChatMessage.query.filter(
            ChatMessage.room_id == room.id,
            ChatMessage.sender_id != user.id,
            ChatMessage.read_at.is_(None),
        )
        .count()
    )


def count_total_unread_messages(user: User) -> int:
    room_ids_query = ChatRoom.query.with_entities(ChatRoom.id).filter(
        or_(ChatRoom.person_user_id == user.id, ChatRoom.enterprise_user_id == user.id)
    )
    return (
        ChatMessage.query.filter(
            ChatMessage.room_id.in_(room_ids_query),
            ChatMessage.sender_id != user.id,
            ChatMessage.read_at.is_(None),
        )
        .count()
    )


def _serialize_room_for_user(room: ChatRoom, user: User) -> dict:
    data = room.to_dict()
    data["unread_count"] = count_unread_messages_for_room(room, user)
    return data


def create_or_get_room_for_property(user: User, property_id: int) -> dict:
    if user.type != "person":
        raise ChatError("Apenas usuários person podem iniciar o chat", 403)

    property_obj = db.session.get(Property, property_id)
    if not property_obj:
        raise ChatError("Imóvel não encontrado", 404)

    visit = (
        Visit.query.filter(
            Visit.property_id == property_id,
            Visit.user_id == user.id,
            Visit.status.in_(VALID_CHAT_VISIT_STATUSES),
        )
        .order_by(Visit.scheduled_at.desc(), Visit.id.desc())
        .first()
    )
    if not visit:
        raise ChatError("É necessário ter uma visita marcada para iniciar este chat", 403)

    room = ChatRoom.query.filter_by(visit_id=visit.id).first()
    if room:
        return room.to_dict()

    room = ChatRoom(
        property_id=property_obj.id,
        visit_id=visit.id,
        person_user_id=user.id,
        enterprise_user_id=property_obj.enterprise_id,
    )
    db.session.add(room)
    db.session.commit()
    return room.to_dict()


def list_rooms_for_user(user: User) -> list[dict]:
    rooms = (
        ChatRoom.query.filter(
            or_(ChatRoom.person_user_id == user.id, ChatRoom.enterprise_user_id == user.id)
        )
        .order_by(
            case((ChatRoom.last_message_at.is_(None), 1), else_=0).asc(),
            ChatRoom.last_message_at.desc(),
            ChatRoom.created_at.desc(),
        )
        .all()
    )
    return [_serialize_room_for_user(room, user) for room in rooms]


def get_room_for_user(room_id: int, user: User) -> dict:
    room = _get_room_entity(room_id)
    _ensure_room_participant(room, user)
    return _serialize_room_for_user(room, user)


def list_messages_for_room(room_id: int, user: User) -> list[dict]:
    room = _get_room_entity(room_id)
    _ensure_room_participant(room, user)
    messages = ChatMessage.query.filter_by(room_id=room.id).order_by(ChatMessage.created_at.asc()).all()
    return [message.to_dict() for message in messages]


def create_message(room_id: int, user: User, content: str) -> dict:
    room = _get_room_entity(room_id)
    _ensure_room_participant(room, user)

    if not isinstance(content, str) or not content.strip():
        raise ChatError("A mensagem não pode ser vazia", 400)

    trimmed_content = content.strip()
    if len(trimmed_content) > 1000:
        raise ChatError("A mensagem deve ter no máximo 1000 caracteres", 400)

    message = ChatMessage(room_id=room.id, sender_id=user.id, content=trimmed_content)
    db.session.add(message)
    db.session.flush()
    room.last_message_at = message.created_at
    db.session.commit()
    return message.to_dict()


def mark_room_messages_as_read(room_id: int, user: User) -> dict:
    room = _get_room_entity(room_id)
    _ensure_room_participant(room, user)

    unread_messages = ChatMessage.query.filter(
        ChatMessage.room_id == room.id,
        ChatMessage.sender_id != user.id,
        ChatMessage.read_at.is_(None),
    ).all()

    if unread_messages:
        read_at = datetime.now(timezone.utc)
        for message in unread_messages:
            message.read_at = read_at
        db.session.commit()

    return {
        "room_id": room.id,
        "marked_count": len(unread_messages),
        "unread_count": count_unread_messages_for_room(room, user),
    }


def get_room_entity_for_user(room_id: int, user: User) -> ChatRoom:
    room = _get_room_entity(room_id)
    _ensure_room_participant(room, user)
    return room


def get_other_participant_id(room_id: int, user: User) -> int:
    room = _get_room_entity(room_id)
    _ensure_room_participant(room, user)
    return _get_other_participant_id(room, user)