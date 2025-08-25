from flask import Blueprint, request, jsonify, abort
from .. import db
from ..models import Question, Category

bp = Blueprint("questions", __name__, url_prefix="/questions")

@bp.post("")
def create_question():
    data = request.get_json() or {}
    text = (data.get("text") or "").strip()
    if not text:
        abort(400, "text is required")
    category_id = data.get("category_id")
    if category_id is not None and not Category.query.get(category_id):
        abort(400, "invalid category_id")
    q = Question(text=text, category_id=category_id)
    db.session.add(q)
    db.session.commit()
    return jsonify({"id": q.id}), 201

@bp.get("")
def list_questions():
    query = Question.query
    category_id = request.args.get("category_id", type=int)
    if category_id:
        query = query.filter(Question.category_id == category_id)
    items = query.all()
    return jsonify([
        {
            "id": q.id,
            "text": q.text,
            "category": {"id": q.category.id, "name": q.category.name} if q.category else None
        } for q in items
    ])
