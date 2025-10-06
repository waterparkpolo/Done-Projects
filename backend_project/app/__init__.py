from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    

    from config import Config
    app.config.from_object(Config)

    db.init_app(app)

    # IMPORTANT: import models BEFORE hooking up migrate,
    # so Alembic sees metadata when it autogenerates
    from . import models  # <-- keep this line

    migrate.init_app(app, db)
    from .routes import api
    app.register_blueprint(api)
    from .routes_auth import auth_bp     
    app.register_blueprint(auth_bp)
    jwt.init_app(app)
    # Error & JWT handlers
    #
    from .errors import register_error_handlers
    from .jwt_handlers import register_jwt_error_handlers
    register_error_handlers(app)
    register_jwt_error_handlers(jwt)
    return app

