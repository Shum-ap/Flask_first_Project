# app/routes/categories.py
from flask import Blueprint, jsonify, request, abort
from app import db
from app.models import Category
from app.schemas.question import CategoryBase

bp = Blueprint("categories", __name__)

@bp.route("/categories", methods=["POST"])
def create_category():
    data = request.get_json()
    try:
        schema = CategoryBase(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    if not schema.name:
        return jsonify({"error": "Name is required"}), 400

    existing = Category.query.filter_by(name=schema.name).first()
    if existing:
        return jsonify({"error": "Category with this name already exists"}), 409

    category = Category(name=schema.name)
    db.session.add(category)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

    return jsonify(category.to_dict()), 201


@bp.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories]), 200


@bp.route("/categories/<int:id>", methods=["PUT"])
def update_category(id):

    category = db.session.get(Category, id)
    if category is None:
        abort(404)

    data = request.get_json()
    try:
        schema = CategoryBase(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    if not schema.name:
        return jsonify({"error": "Name is required"}), 400

    conflict = Category.query.filter(Category.name == schema.name, Category.id != id).first()
    if conflict:
        return jsonify({"error": "Another category has this name"}), 409

    category.name = schema.name
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

    return jsonify(category.to_dict()), 200


@bp.route("/categories/<int:id>", methods=["DELETE"])
def delete_category(id):

    category = db.session.get(Category, id)
    if category is None:
        abort(404)

    if len(category.questions) > 0:
        return jsonify({"error": "Cannot delete category with assigned questions"}), 400

    db.session.delete(category)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

    return jsonify({"message": "Category deleted"}), 200