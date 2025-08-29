# app/routes/questions.py
from flask import Blueprint, jsonify, request
from app import db
from app.models import Question, Category
from app.schemas.question import QuestionCreate

bp = Blueprint("questions", __name__, url_prefix="/api")


@bp.route("/questions", methods=["GET"])
def get_questions():
    questions = Question.query.all()
    return jsonify([q.to_dict() for q in questions])


@bp.route("/questions", methods=["POST"])
def create_question():
    data = request.get_json()

    try:
        schema = QuestionCreate(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    if not schema.text or not schema.answer:
        return jsonify({"error": "Text and answer are required"}), 400

    if schema.category_id:
        category = db.session.get(Category, schema.category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

    question = Question(
        text=schema.text,
        answer=schema.answer,
        category_id=schema.category_id
    )
    db.session.add(question)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Failed to create question"}), 500

    return jsonify(question.to_dict()), 201