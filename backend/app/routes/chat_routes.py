from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields

from app.services.auth_service import token_required
from app.services.chat_service import (
    ChatError,
    count_total_unread_messages,
    create_message,
    create_or_get_room_for_property,
    get_room_for_user,
    list_messages_for_room,
    list_rooms_for_user,
    mark_room_messages_as_read,
)

chat_bp = Blueprint("chat", __name__, url_prefix="/chats")


class CreateChatSchema(Schema):
    property_id = fields.Integer(required=True)


class CreateMessageSchema(Schema):
    content = fields.String(required=True)


create_chat_schema = CreateChatSchema()
create_message_schema = CreateMessageSchema()


@chat_bp.route("", methods=["POST"])
@token_required
def route_create_chat(current_user):
    errors = create_chat_schema.validate(request.json or {})
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        room = create_or_get_room_for_property(current_user, request.json["property_id"])
        return jsonify(room), 201
    except ChatError as exc:
        return jsonify({"error": str(exc)}), exc.status_code


@chat_bp.route("", methods=["GET"])
@token_required
def route_list_chats(current_user):
    return jsonify(list_rooms_for_user(current_user)), 200


@chat_bp.route("/unread-count", methods=["GET"])
@token_required
def route_get_unread_count(current_user):
    return jsonify({"unread_count": count_total_unread_messages(current_user)}), 200


@chat_bp.route("/<int:room_id>", methods=["GET"])
@token_required
def route_get_chat(current_user, room_id):
    try:
        return jsonify(get_room_for_user(room_id, current_user)), 200
    except ChatError as exc:
        return jsonify({"error": str(exc)}), exc.status_code


@chat_bp.route("/<int:room_id>/messages", methods=["GET"])
@token_required
def route_get_chat_messages(current_user, room_id):
    try:
        return jsonify(list_messages_for_room(room_id, current_user)), 200
    except ChatError as exc:
        return jsonify({"error": str(exc)}), exc.status_code


@chat_bp.route("/<int:room_id>/messages", methods=["POST"])
@token_required
def route_create_chat_message(current_user, room_id):
    errors = create_message_schema.validate(request.json or {})
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        return jsonify(create_message(room_id, current_user, request.json["content"])), 201
    except ChatError as exc:
        return jsonify({"error": str(exc)}), exc.status_code


@chat_bp.route("/<int:room_id>/read", methods=["POST"])
@token_required
def route_mark_chat_as_read(current_user, room_id):
    try:
        return jsonify(mark_room_messages_as_read(room_id, current_user)), 200
    except ChatError as exc:
        return jsonify({"error": str(exc)}), exc.status_code