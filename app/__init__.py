from flask import Flask
from flask_cors import CORS


def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    if not app.config['TESTING']:
        from app.db_manager import DatabaseManager
        DatabaseManager.open_database()

    # Registering blueprints
    from app.routes.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.routes.todo import todo_blueprint
    app.register_blueprint(todo_blueprint)

    from flask_jwt_extended import JWTManager
    JWTManager(app)

    return app
