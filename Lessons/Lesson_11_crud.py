from dataclasses import dataclass
from flask import Flask, request, jsonify
from typing import Optional, List

app = Flask(__name__)

# --- Data Classes ---
@dataclass
class QuestionData:
    id: int
    text: str

@dataclass
class ErrorResponse:
    error: str

@dataclass
class SuccessResponse:
    message: str
    id: Optional[int] = None

# --- "База данных" в памяти ---
questions_db: List[QuestionData] = []
next_id = 1  # Автоинкремент ID

# --- Routes ---

# Получить все вопросы
@app.route('/questions', methods=['GET'])
def get_questions():
    return jsonify([q.__dict__ for q in questions_db]), 200

# Создать новый вопрос
@app.route('/questions', methods=['POST'])
def create_question():
    global next_id
    json_data = request.get_json()
    if not json_data or 'text' not in json_data:
        error_response = ErrorResponse("No question text provided")
        return jsonify(error_response.__dict__), 400

    question = QuestionData(id=next_id, text=json_data['text'])
    questions_db.append(question)
    next_id += 1

    success_response = SuccessResponse("Вопрос создан", question.id)
    return jsonify(success_response.__dict__), 201

# Получить вопрос по ID
@app.route('/questions/<int:id>', methods=['GET'])
def get_question(id: int):
    question = next((q for q in questions_db if q.id == id), None)
    if not question:
        error_response = ErrorResponse("Вопрос с таким ID не найден")
        return jsonify(error_response.__dict__), 404
    return jsonify(question.__dict__), 200

# Обновить вопрос по ID
@app.route('/questions/<int:id>', methods=['PUT'])
def update_question(id: int):
    json_data = request.get_json()
    if not json_data or 'text' not in json_data:
        error_response = ErrorResponse("Текст вопроса не предоставлен")
        return jsonify(error_response.__dict__), 400

    question = next((q for q in questions_db if q.id == id), None)
    if not question:
        error_response = ErrorResponse("Вопрос с таким ID не найден")
        return jsonify(error_response.__dict__), 404

    question.text = json_data['text']
    success_response = SuccessResponse(f"Вопрос обновлен: {question.text}", question.id)
    return jsonify(success_response.__dict__), 200

# Удалить вопрос по ID
@app.route('/questions/<int:id>', methods=['DELETE'])
def delete_question(id: int):
    global questions_db
    question = next((q for q in questions_db if q.id == id), None)
    if not question:
        error_response = ErrorResponse("Вопрос с таким ID не найден")
        return jsonify(error_response.__dict__), 404

    questions_db = [q for q in questions_db if q.id != id]
    success_response = SuccessResponse(f"Вопрос с ID {id} удален", id)
    return jsonify(success_response.__dict__), 200

# --- Запуск приложения ---
if __name__ == '__main__':
    app.run(debug=True)
