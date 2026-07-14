from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, validate

from app.services.auth_service import token_required
from app.services.visit_service import (
    VisitError,
    create_visit as create_visit_service,
    get_visit_by_id,
    list_visits,
    list_visits_for_enterprise,
    update_visit_status,
)

visit_bp = Blueprint("visits", __name__, url_prefix="/visits")


class CreateVisitSchema(Schema):
    property_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    scheduled_at = fields.DateTime(required=True)
    status = fields.String(validate=validate.OneOf(["pending", "confirmed", "cancelled"]))
    note = fields.String(validate=validate.Length(max=500))


create_visit_schema = CreateVisitSchema()


@visit_bp.route("", methods=["POST"])
def route_create_visit():
    errors = create_visit_schema.validate(request.json or {})
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        visit = create_visit_service(request.json or {})
        return jsonify(visit), 201
    except VisitError as exc:
        return jsonify({"error": str(exc)}), 400


@visit_bp.route("", methods=["GET"])
def route_list_visits():
    property_id = request.args.get("property_id", type=int)
    user_id = request.args.get("user_id", type=int)
    return jsonify(list_visits(property_id=property_id, user_id=user_id)), 200


@visit_bp.route("/me", methods=["GET"])
@token_required
def route_list_my_visits(current_user):
    return jsonify(list_visits(user_id=current_user.id)), 200


@visit_bp.route("/received", methods=["GET"])
@token_required
def route_list_received_visits(current_user):
    if current_user.type != "enterprise":
        return jsonify({"error": "Only enterprise users have received visits"}), 403
    return jsonify(list_visits_for_enterprise(current_user.id)), 200


@visit_bp.route("/<int:visit_id>", methods=["GET"])
def route_get_visit(visit_id):
    visit = get_visit_by_id(visit_id)
    if not visit:
        return jsonify({"error": "Visit not found"}), 404
    return jsonify(visit), 200


@visit_bp.route("/<int:visit_id>/status", methods=["PATCH"])
@token_required
def route_update_visit_status(current_user, visit_id):
    payload = request.json or {}
    status = payload.get("status")
    if not status:
        return jsonify({"error": "status is required"}), 400

    try:
        visit = update_visit_status(
            visit_id, status, acting_user_id=current_user.id
        )
        return jsonify(visit), 200
    except PermissionError as exc:
        return jsonify({"error": str(exc)}), 403
    except VisitError as exc:
        if str(exc) == "Visit not found":
            return jsonify({"error": str(exc)}), 404
        return jsonify({"error": str(exc)}), 400
