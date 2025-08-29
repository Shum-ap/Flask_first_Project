from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.models import db
from app.models.questions import Question
from app.schemas.questions import QuestionCreate, QuestionResponse, MessageResponse  # <- исправлено

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')
# Получение всех вопросов
@questions_bp.route('/', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    results = [QuestionResponse.from_orm(q).dict() for q in questions]
    return jsonify(results), 200

# Создание нового вопроса
@questions_bp.route('/', methods=['POST'])
def create_question():
    json_data = request.get_json()
    try:
        data = QuestionCreate(**json_data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    question = Question(text=data.text)
    db.session.add(question)
    db.session.commit()

    response = QuestionResponse.from_orm(question)
    return jsonify(response.dict()), 201

# Получение вопроса по ID
@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    question = Question.query.get(id)
    if not question:
        return jsonify(MessageResponse(message="Вопрос с таким ID не найден").dict()), 404
    return jsonify(QuestionResponse.from_orm(question).dict()), 200
