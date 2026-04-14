from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__)


@api_bp.route("/health")
def health_check():
    """Verifica se a API e o banco de dados estao funcionando.
    ---
    tags:
      - Status
    responses:
      200:
        description: Status da API e conexao com o banco
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
            database:
              type: string
              example: connected
    """
    from app import db

    try:
        db.session.execute(db.text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return jsonify({"status": "ok", "database": db_status})
