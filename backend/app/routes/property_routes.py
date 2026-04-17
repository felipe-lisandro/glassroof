from datetime import date

from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, validate

from app.services.property_service import (
    create_property as create_property_service,
    get_all_properties,
    get_property_by_id,
    get_properties_from_enterprise,
)

from app.services.auth_service import token_required

property_bp = Blueprint("properties", __name__, url_prefix="/properties")


# --------------- Validation schemas ---------------

class PropertySchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    description = fields.String(required=True, validate=validate.Length(min=1, max=300))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    overall_rating = fields.Float(validate=validate.Range(min=0, max=5))
    register_date = fields.Date()

class ImageSchema(Schema):
    URL = fields.String(required=True, validate=validate.Length(min=1, max=400))
    order = fields.Integer(required=True, validate=validate.Range(min=0))
    size_mb = fields.Integer(required=True, validate=validate.Range(min=0))
    description = fields.String(required=True, validate=validate.Length(min=1, max=200))

class LocationSchema(Schema):
    street = fields.String(required=True, validate=validate.Length(min=1, max=120))
    number = fields.Integer(required=True)
    CEP = fields.String(required=True, validate=validate.Length(min=1, max=20))
    complement = fields.String(validate=validate.Length(max=300))
    city = fields.String(required=True, validate=validate.Length(min=1, max=120))
    state = fields.String(required=True, validate=validate.Length(min=1, max=120))
    country = fields.String(required=True, validate=validate.Length(min=1, max=120))

class CreatePropertySchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    description = fields.String(required=True, validate=validate.Length(min=1, max=300))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    overall_rating = fields.Float(validate=validate.Range(min=0, max=5))
    register_date = fields.Date()
    enterprise_id = fields.Integer(required=True)
    location = fields.Nested(LocationSchema, required=True)
    images = fields.List(fields.Nested(ImageSchema), required=True)


create_property_schema = CreatePropertySchema()


# --------------- Routes ---------------

@property_bp.route("/", methods=["POST"])
@token_required
def create_property(current_user):
    """Cria uma nova propriedade.
    ---
    tags:
      - Propriedades
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - description
            - price
            - enterprise_id
            - location
            - images
          properties:
            name:
              type: string
              example: Pedro
            description:
              type: string
              example: Propriedade em condomínio
            price:
              type: number
              format: float
              example: 500000.0
            enterprise_id:
              type: integer
              example: 1
            location:
              type: object
              required:
                - street
                - number
                - CEP
                - city
                - state
                - country
              properties:
                street:
                  type: string
                  example: Rua das Flores
                number:
                  type: integer
                  example: 123
                CEP:
                  type: string
                  example: 12345-678
                complement:
                  type: string
                  example: Apto 101
                city:
                  type: string
                  example: São Paulo
                state:
                  type: string
                  example: SP
                country:
                  type: string
                  example: Brasil
            images:
              type: array
              items:
                type: object
                required:
                  - URL
                  - order
                  - size_mb
                  - description
                properties:
                  URL:
                    type: string
                    example: https://example.com/image.jpg
                  order:
                    type: integer
                    example: 1
                  size_mb:
                    type: integer
                    example: 2
                  description:
                    type: string
                    example: Imagem da fachada
    responses:
      201:
        description: Propriedade criada com sucesso
      400:
        description: Dados invalidos
    """
    if current_user.type != "enterprise":
        return jsonify({"error": "Apenas usuários do tipo 'enterprise' podem criar propriedades"}), 403
    
    errors = create_property_schema.validate(request.json)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        property = create_property_service(request.json)
        return jsonify(property), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@property_bp.route("/enterprise/<int:enterprise_id>", methods=["GET"])
def route_get_properties_from_enterprise(enterprise_id):
    """Obtém todas as propriedades de uma empresa.
    ---
    tags:
      - Propriedades
    parameters:
      - in: path
        name: enterprise_id
        type: integer
        required: true
    responses:
      200:
        description: Lista de propriedades
      400:
        description: Erro
    """
    try:
        properties = get_properties_from_enterprise(enterprise_id)
        return jsonify(properties), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@property_bp.route("", methods=["GET"])
def route_get_all_properties():
    """Obtém todas as propriedades.
    ---
    tags:
      - Propriedades
    responses:
      200:
        description: Lista de propriedades
      400:
        description: Erro
    """
    try:
        properties = get_all_properties()
        return jsonify(properties), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@property_bp.route("/<int:property_id>", methods=["GET"])
def route_get_property_by_id(property_id):
    """Obtém uma propriedade pelo ID.
    ---
    tags:
      - Propriedades
    responses:
      200:
        description: Lista de propriedades
      400:
        description: Erro
    """
    try:
        property = get_property_by_id(property_id)
        return jsonify(property), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400