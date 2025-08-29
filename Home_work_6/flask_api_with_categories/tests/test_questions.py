# tests/test_questions.py
def test_get_questions_empty(client, empty_db):
    """Проверка: GET /api/questions — пустой список"""
    response = client.get("/api/questions")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_question(client, init_database):
    """Проверка: POST /api/questions — создание вопроса с категорией"""
    science_id = init_database['science_id']
    response = client.post("/api/questions", json={
        "text": "What is 2+2?",
        "answer": "4",
        "category_id": science_id
    })
    data = response.get_json()

    assert response.status_code == 201
    assert data["text"] == "What is 2+2?"
    assert data["answer"] == "4"
    assert data["category_id"] == science_id
    assert data["category"]["name"] == "Science"


def test_create_question_no_text(client, init_database):
    """Проверка: ошибка, если не передан text"""
    response = client.post("/api/questions", json={
        "answer": "Test",
        "category_id": 1
    })
    assert response.status_code == 400


def test_create_question_invalid_category(client, empty_db):
    """Проверка: ошибка, если category_id не существует"""
    response = client.post("/api/questions", json={
        "text": "Invalid",
        "answer": "Test",
        "category_id": 999
    })
    assert response.status_code == 404


def test_get_questions_with_category(client, init_database):
    """Проверка: GET /api/questions — возвращает вопросы с категориями"""
    response = client.get("/api/questions")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 3
    for q in data:
        assert "category" in q
        if q["category"]:
            assert "id" in q["category"]
            assert "name" in q["category"]