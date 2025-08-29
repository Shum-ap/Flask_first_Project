from app import create_app, db
from app.models import Category, Question
import json

app = create_app()

with app.app_context():
    # Получаем все категории
    categories = [{"id": c.id, "name": c.name} for c in Category.query.all()]

    # Получаем все вопросы
    questions = [{"id": q.id, "text": q.text, "category_id": q.category_id} for q in Question.query.all()]

    # Выводим красиво
    print(json.dumps({"categories": categories, "questions": questions}, ensure_ascii=False, indent=2))
