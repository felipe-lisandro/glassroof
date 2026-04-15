from datetime import date

from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, validate

from app.services.user_service import (
    DuplicateError,
    create_enterprise_user,
    create_person_user,
    get_all_users,
    get_user_by_id,
)

user_bp = Blueprint("users", __name__, url_prefix="/users")


# --------------- Validation schemas ---------------

class PersonUserSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    cpf = fields.String(required=True, validate=validate.Length(equal=11))
    last_name = fields.String(validate=validate.Length(max=120))
    birthday = fields.Date()


class EnterpriseUserSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    cnpj = fields.String(required=True, validate=validate.Length(equal=14))


person_schema = PersonUserSchema()
enterprise_schema = EnterpriseUserSchema()


# --------------- Routes ---------------

@user_bp.route("/person", methods=["POST"])
def register_person():
    """Cadastra uma pessoa fisica.
    ---
    tags:
      - Usuarios
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - password
            - cpf
          properties:
            name:
              type: string
              example: Pedro
            email:
              type: string
              example: pedro@email.com
            password:
              type: string
              example: "123456"
            cpf:
              type: string
              example: "12345678901"
            last_name:
              type: string
              example: Martins
            birthday:
              type: string
              format: date
              example: "2000-01-15"
    responses:
      201:
        description: Usuario criado com sucesso
      400:
        description: Dados invalidos
      409:
        description: Email ou CPF ja cadastrado
    """
    if isinstance(request.json["birthday"], str):
      from datetime import datetime
      request.json["birthday"] = datetime.strptime(request.json["birthday"], "%Y-%m-%d").date()
    errors = person_schema.validate(request.json)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        user = create_person_user(request.json)
        return jsonify(user), 201
    except DuplicateError as e:
        return jsonify({"error": str(e)}), 409


@user_bp.route("/enterprise", methods=["POST"])
def register_enterprise():
    """Cadastra uma pessoa juridica.
    ---
    tags:
      - Usuarios
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - password
            - cnpj
          properties:
            name:
              type: string
              example: Imobiliaria XYZ
            email:
              type: string
              example: contato@xyz.com
            password:
              type: string
              example: "123456"
            cnpj:
              type: string
              example: "12345678000199"
    responses:
      201:
        description: Empresa criada com sucesso
      400:
        description: Dados invalidos
      409:
        description: Email ou CNPJ ja cadastrado
    """
    errors = enterprise_schema.validate(request.json)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        user = create_enterprise_user(request.json)
        return jsonify(user), 201
    except DuplicateError as e:
        return jsonify({"error": str(e)}), 409


@user_bp.route("", methods=["GET"])
def list_users():
    """Lista todos os usuarios cadastrados.
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de usuarios
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              email:
                type: string
              register_date:
                type: string
              type:
                type: string
    """
    users = get_all_users()
    return jsonify(users)


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Busca um usuario por ID.
    ---
    tags:
      - Usuarios
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
    responses:
      200:
        description: Dados do usuario
      404:
        description: Usuario nao encontrado
    """
    user = get_user_by_id(user_id)
    if user is None:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return jsonify(user)
