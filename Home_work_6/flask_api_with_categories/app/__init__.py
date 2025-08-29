# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    # Регистрация блюпринтов с префиксом /api
    from .routes.questions import bp as questions_bp
    from .routes.categories import bp as categories_bp

    # Регистрируем блюпринты с префиксом /api
    app.register_blueprint(questions_bp, url_prefix='/api')
    app.register_blueprint(categories_bp, url_prefix='/api')

    # Добавляем маршрут для главной страницы
    @app.route("/")
    def home():
        return {
            "message": "Welcome to the Quiz API!",
            "status": "OK",
            "endpoints": {
                "categories": "/api/categories",
                "questions": "/api/questions"
            }
        }

    return app