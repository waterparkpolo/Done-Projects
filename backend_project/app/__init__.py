from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

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
    return app
