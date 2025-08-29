# app/models.py
from . import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    questions = db.relationship("Question", back_populates="category")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __repr__(self):
        return f"<Category '{self.name}'>"


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)  # ← добавлено, так как используется в схемах

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    category = db.relationship("Category", back_populates="questions")

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "answer": self.answer,
            "category_id": self.category_id,
            "category": self.category.to_dict() if self.category else None
        }

    def __repr__(self):
        return f"<Question '{self.text[:30]}...'>"