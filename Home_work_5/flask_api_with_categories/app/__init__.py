from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    from .routes.questions import bp as questions_bp
    from .routes.categories import bp as categories_bp
    app.register_blueprint(questions_bp)
    app.register_blueprint(categories_bp)

    return app
