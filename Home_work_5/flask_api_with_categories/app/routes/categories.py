from flask import Blueprint, request, jsonify, abort
from .. import db
from ..models import Category

bp = Blueprint("categories", __name__, url_prefix="/categories")

@bp.post("")
def create_category():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    if not name:
        abort(400, "name is required")
    if Category.query.filter_by(name=name).first():
        abort(409, "category already exists")
    c = Category(name=name)
    db.session.add(c)
    db.session.commit()
    return jsonify({"id": c.id, "name": c.name}), 201

@bp.get("")
def list_categories():
    items = Category.query.order_by(Category.name.asc()).all()
    return jsonify([{"id": c.id, "name": c.name} for c in items])
