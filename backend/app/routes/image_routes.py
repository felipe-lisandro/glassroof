from flask import Blueprint, jsonify, request

from marshmallow import Schema, fields, validate

from app.services.image_service import (
    create_image,
    get_image_by_id,
    get_images_by_property,
)

image_bp = Blueprint("images", __name__, url_prefix="/images")


# --------------- Validation schemas ---------------

class ImageSchema(Schema):
    url = fields.String(required=True, validate=validate.Length(min=1, max=400))
    property_id = fields.Integer(required=True)
    order = fields.Integer(required=True, validate=validate.Range(min=0))
    size_mb = fields.Integer(required=True, validate=validate.Range(min=0))
    description = fields.String(required=True, validate=validate.Length(min=1, max=200))

image_schema = ImageSchema()

# --------------- Routes ---------------

@image_bp.route("/", methods=["POST"])
def create_image():
    """Cria uma nova imagem.
    ---
    tags:
      - Imagens
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - url
            - property_id
          properties:
            url:
              type: string
              example: https://example.com/image.jpg
            property_id:
              type: integer
              example: 1
    responses:
      201:
        description: Imagem criada com sucesso
      400:
        description: Dados invalidos
    """
    
    errors = image_schema.validate(request.json)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        image = create_image(request.json)
        return jsonify(image), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@image_bp.route("/property/<int:property_id>", methods=["GET"])
def get_images_by_property(property_id):
    """Obtém todas as imagens de uma propriedade.
    ---
    tags:
      - Imagens
    parameters:
      - in: path
        name: property_id
        type: integer
        required: true
    responses:
      200:
        description: Lista de imagens
      400:
        description: Erro
    """
    try:
        images = get_images_by_property(property_id)
        return jsonify(images), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    
@image_bp.route("/<int:image_id>", methods=["GET"])
def get_image_by_id(image_id):
    """Obtém uma imagem pelo ID.
    ---
    tags:
      - Imagens
    responses:
      200:
        description: Imagem encontrada
      400:
        description: Erro
    """
    try:
        image = get_image_by_id(image_id)
        return jsonify(image), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400