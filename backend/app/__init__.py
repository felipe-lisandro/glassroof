from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

from app.config import Config

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")

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
    socketio.init_app(app)
    Swagger(app, template=SWAGGER_TEMPLATE)

    from app.routes import api_bp
    from app.routes.general_routes import general_bp
    from app.routes.user_routes import user_bp
    from app.routes.property_routes import property_bp
    from app.routes.visit_routes import visit_bp
    from app.routes.chat_routes import chat_bp
    from app.socket_events import register_socket_events

    app.register_blueprint(api_bp)
    app.register_blueprint(general_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(property_bp)
    app.register_blueprint(visit_bp)
    app.register_blueprint(chat_bp)
    register_socket_events(socketio)

    with app.app_context():
        from app import models  # noqa: F401 — ensure models are registered
        db.create_all()

    return app
