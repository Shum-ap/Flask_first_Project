from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routers.questions import questions_bp
from app.routers.response import response_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(questions_bp)
    app.register_blueprint(response_bp)

    return app
