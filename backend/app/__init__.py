from flasgger import Swagger
from flask import Flask, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()

SWAGGER_TEMPLATE = {
    "info": {
        "title": "Glassroof API",
        "description": "API do sistema Glassroof Imobiliário",
        "version": "0.1.0",
    },
}


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)
    db.init_app(app)
    Swagger(app, template=SWAGGER_TEMPLATE)

    from app.routes import api_bp
    from app.routes.user_routes import user_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(user_bp)

    @app.route("/")
    def index():
        return redirect("/apidocs")

    with app.app_context():
        from app import models  # noqa: F401 — ensure models are registered
        db.create_all()

    return app
