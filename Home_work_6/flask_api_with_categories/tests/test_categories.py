# tests/test_categories.py
import json


def test_get_categories_empty(client, empty_db):
    """Проверка: GET /api/categories — пустой список"""
    response = client.get("/api/categories")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_category(client, empty_db):
    """Проверка: POST /api/categories — создание новой категории"""
    response = client.post("/api/categories", json={"name": "Programming"})
    data = response.get_json()

    assert response.status_code == 201
    assert data["name"] == "Programming"
    assert "id" in data


def test_create_category_duplicate(client, init_database):
    """Проверка: нельзя создать категорию с существующим именем"""
    response = client.post("/api/categories", json={"name": "Science"})
    assert response.status_code == 409  # Conflict
    assert "error" in response.get_json()


def test_get_categories_with_data(client, init_database):
    """Проверка: GET /api/categories — возвращает список с данными"""
    response = client.get("/api/categories")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 3
    category_names = {c["name"] for c in data}
    assert "Science" in category_names
    assert "History" in category_names
    assert "Programming" in category_names


def test_update_category(client, init_database):
    """Проверка: PUT /api/categories/{id} — обновление категории"""
    science_id = init_database['science_id']
    response = client.put(f"/api/categories/{science_id}", json={"name": "Physics"})
    data = response.get_json()

    assert response.status_code == 200
    assert data["name"] == "Physics"


def test_update_category_not_found(client, empty_db):
    """Проверка: обновление несуществующей категории"""
    response = client.put("/api/categories/999", json={"name": "Not Found"})
    assert response.status_code == 404


def test_delete_category(client, init_database):
    """Проверка: DELETE /api/categories/{id} — удаление категории без вопросов"""
    programming_id = init_database['programming_id']

    # Сначала удалим вопрос, чтобы можно было удалить категорию
    with client.application.app_context():
        from app.models import Question, db
        Question.query.filter_by(category_id=programming_id).delete()
        db.session.commit()

    response = client.delete(f"/api/categories/{programming_id}")
    assert response.status_code == 200
    assert "message" in response.get_json()


def test_delete_category_with_questions(client, init_database):
    """Проверка: нельзя удалить категорию, если есть вопросы"""
    science_id = init_database['science_id']
    response = client.delete(f"/api/categories/{science_id}")
    assert response.status_code == 400
    assert "error" in response.get_json()