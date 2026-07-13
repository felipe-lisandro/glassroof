from datetime import date

from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, validate

from app.services.property_service import (
    create_property as create_property_service,
    get_all_properties,
    get_property_by_id,
    get_properties_from_enterprise,
)
from app.services.avaliation_service import (
    create_avaliation as create_avaliation_service,
    list_avaliations as list_avaliations_service,
  update_avaliation as update_avaliation_service,
  delete_avaliation as delete_avaliation_service,
      create_avaliations_bulk as create_avaliations_bulk_service,
)
from app.services.catergory_service import list_categories as list_categories_service

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


class CreateAvaliationSchema(Schema):
    user_id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    comment = fields.String(required=True, validate=validate.Length(min=1, max=500))
    stars = fields.Integer(required=True, validate=validate.Range(min=0, max=5))
    photos = fields.List(fields.String(validate=validate.Length(min=1, max=400)), load_default=[])

class BulkAvaliationItemSchema(Schema):
    category_id = fields.Integer(required=True)
    comment = fields.String(required=True, validate=validate.Length(min=1, max=500))
    stars = fields.Integer(required=True, validate=validate.Range(min=0, max=5))
    photos = fields.List(fields.String(validate=validate.Length(min=1, max=400)), load_default=[])

class BulkCreateAvaliationSchema(Schema):
    user_id = fields.Integer(required=True)
    avaliations = fields.List(fields.Nested(BulkAvaliationItemSchema), required=True, validate=validate.Length(min=1))


class UpdateAvaliationSchema(Schema):
    comment = fields.String(required=True, validate=validate.Length(min=1, max=500))
    stars = fields.Integer(required=True, validate=validate.Range(min=0, max=5))
    photos = fields.List(fields.String(validate=validate.Length(min=1, max=400)), load_default=[])


create_property_schema = CreatePropertySchema()
create_avaliation_schema = CreateAvaliationSchema()
bulk_create_avaliation_schema = BulkCreateAvaliationSchema()
update_avaliation_schema = UpdateAvaliationSchema()


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


@property_bp.route("/categories", methods=["GET"])
def route_list_categories():
    """Lista categorias globais de avaliação.
    ---
    tags:
      - Categorias
    responses:
      200:
        description: Lista de categorias
      400:
        description: Erro
    """
    try:
        categories = list_categories_service()
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@property_bp.route("/<int:property_id>/avaliations", methods=["POST"])
def route_create_avaliation(property_id):
    """Cria uma avaliação para um imóvel.
    ---
    tags:
      - Avaliações
    parameters:
      - in: path
        name: property_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - user_id
            - category_id
            - comment
            - stars
          properties:
            user_id:
              type: integer
              example: 2
            category_id:
              type: integer
              example: 1
            comment:
              type: string
              example: Imóvel excelente.
            stars:
              type: integer
              minimum: 0
              maximum: 5
              example: 5
            photos:
              type: array
              items:
                type: string
              example: ["https://example.com/photo1.jpg"]
    responses:
      201:
        description: Avaliação criada com sucesso
      400:
        description: Dados inválidos
      404:
        description: Imóvel não encontrado
    """
    errors = create_avaliation_schema.validate(request.json or {})
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        avaliation = create_avaliation_service(property_id, request.json or {})
        return jsonify(avaliation), 201
    except ValueError as exc:
        if str(exc) in {"Property not found", "Category not found", "User not found"}:
            return jsonify({"error": str(exc)}), 404
        return jsonify({"error": str(exc)}), 400

@property_bp.route("/<int:property_id>/avaliations/bulk", methods=["POST"])
def route_create_avaliations_bulk(property_id):
    """Cria várias avaliações de um imóvel em lote (uma por categoria).
    ---
    tags:
      - Avaliações
    responses:
      201:
        description: Avaliações criadas com sucesso
      400:
        description: Dados inválidos
      404:
        description: Imóvel, usuário ou categoria não encontrado
    """
    errors = bulk_create_avaliation_schema.validate(request.json or {})
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        avaliations = create_avaliations_bulk_service(property_id, request.json or {})
        return jsonify(avaliations), 201
    except ValueError as exc:
        if str(exc) in {"Property not found", "Category not found", "User not found"}:
            return jsonify({"error": str(exc)}), 404
        return jsonify({"error": str(exc)}), 400


@property_bp.route("/<int:property_id>/avaliations", methods=["GET"])
def route_list_avaliations(property_id):
    """Lista avaliações de um imóvel, com opcional filtro por estrelas.
    ---
    tags:
      - Avaliações
    parameters:
      - in: path
        name: property_id
        type: integer
        required: true
      - in: query
        name: stars
        type: integer
        required: false
    responses:
      200:
        description: Lista de avaliações
      400:
        description: Filtro inválido
      404:
        description: Imóvel não encontrado
    """
    try:
        avaliations = list_avaliations_service(property_id, request.args.get("stars"))
        return jsonify(avaliations), 200
    except ValueError as exc:
        if str(exc) == "Property not found":
            return jsonify({"error": str(exc)}), 404
        return jsonify({"error": str(exc)}), 400


@property_bp.route("/<int:property_id>/avaliations/<int:avaliation_id>", methods=["PUT"])
@token_required
def route_update_avaliation(current_user, property_id, avaliation_id):
    """Atualiza uma avaliação do próprio usuário.
    ---
    tags:
      - Avaliações
    responses:
      200:
        description: Avaliação atualizada
      400:
        description: Dados inválidos
      403:
        description: Sem permissão para alterar a avaliação
      404:
        description: Avaliação não encontrada
    """
    errors = update_avaliation_schema.validate(request.json or {})
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        updated = update_avaliation_service(property_id, avaliation_id, current_user.id, request.json or {})
        return jsonify(updated), 200
    except PermissionError as exc:
        return jsonify({"error": str(exc)}), 403
    except ValueError as exc:
        if str(exc) == "Avaliation not found":
            return jsonify({"error": str(exc)}), 404
        return jsonify({"error": str(exc)}), 400


@property_bp.route("/<int:property_id>/avaliations/<int:avaliation_id>", methods=["DELETE"])
@token_required
def route_delete_avaliation(current_user, property_id, avaliation_id):
    """Remove uma avaliação do próprio usuário.
    ---
    tags:
      - Avaliações
    responses:
      204:
        description: Avaliação removida
      403:
        description: Sem permissão para excluir a avaliação
      404:
        description: Avaliação não encontrada
    """
    try:
        delete_avaliation_service(property_id, avaliation_id, current_user.id)
        return "", 204
    except PermissionError as exc:
        return jsonify({"error": str(exc)}), 403
    except ValueError as exc:
        if str(exc) == "Avaliation not found":
            return jsonify({"error": str(exc)}), 404
        return jsonify({"error": str(exc)}), 400
    
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