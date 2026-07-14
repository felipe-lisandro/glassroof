from flask_socketio import disconnect, emit, join_room, leave_room

from app import db
from app.models.user import User
from app.services.auth_service import get_user_from_token
from app.services.chat_service import (
    ChatError,
    count_total_unread_messages,
    create_message,
    get_other_participant_id,
    get_room_channel,
    get_room_entity_for_user,
    get_user_channel,
    mark_room_messages_as_read,
)


def register_socket_events(socketio):
    @socketio.on("connect")
    def handle_connect(auth):
        token = (auth or {}).get("token")
        if not token:
            return False

        try:
            user = get_user_from_token(token)
            if not user:
                return False
            join_room(get_user_channel(user.id))
            emit("unread_count_updated", {"unread_count": count_total_unread_messages(user)})
            return True
        except Exception:
            return False

    @socketio.on("join_chat")
    def handle_join_chat(payload):
        token = (payload or {}).get("token")
        room_id = (payload or {}).get("room_id")
        if not token or room_id is None:
            emit("chat_error", {"error": "token e room_id são obrigatórios"})
            return

        try:
            user = get_user_from_token(token)
            if not user:
                emit("chat_error", {"error": "Usuário inválido"})
                disconnect()
                return
            get_room_entity_for_user(int(room_id), user)
            join_room(get_room_channel(int(room_id)))
            mark_room_messages_as_read(int(room_id), user)
            emit("unread_count_updated", {"unread_count": count_total_unread_messages(user)}, to=get_user_channel(user.id))
            emit("chat_joined", {"room_id": int(room_id)})
        except ChatError as exc:
            emit("chat_error", {"error": str(exc), "status_code": exc.status_code})
        except Exception:
            emit("chat_error", {"error": "Falha ao entrar na sala"})

    @socketio.on("leave_chat")
    def handle_leave_chat(payload):
        room_id = (payload or {}).get("room_id")
        if room_id is None:
            return
        leave_room(get_room_channel(int(room_id)))

    @socketio.on("send_message")
    def handle_send_message(payload):
        token = (payload or {}).get("token")
        room_id = (payload or {}).get("room_id")
        content = (payload or {}).get("content")
        if not token or room_id is None:
            emit("chat_error", {"error": "token e room_id são obrigatórios"})
            return

        try:
            user = get_user_from_token(token)
            if not user:
                emit("chat_error", {"error": "Usuário inválido"})
                disconnect()
                return
            message = create_message(int(room_id), user, content)
            recipient_id = get_other_participant_id(int(room_id), user)
            emit("message_created", message, to=get_room_channel(int(room_id)))
            emit(
                "unread_count_updated",
                {"unread_count": count_total_unread_messages(user)},
                to=get_user_channel(user.id),
            )
            recipient = db.session.get(User, recipient_id)
            if recipient:
                emit(
                    "unread_count_updated",
                    {"unread_count": count_total_unread_messages(recipient)},
                    to=get_user_channel(recipient.id),
                )
        except ChatError as exc:
            emit("chat_error", {"error": str(exc), "status_code": exc.status_code})
        except Exception:
            emit("chat_error", {"error": "Falha ao enviar mensagem"})