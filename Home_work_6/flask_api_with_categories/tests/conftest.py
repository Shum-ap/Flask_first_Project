# tests/conftest.py
import os
import tempfile
import pytest
from app import create_app, db


@pytest.fixture
def app():
    """Создаём тестовое приложение с временной БД"""
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)

    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        db.create_all()

    yield app

    # Удаляем временный файл БД после теста
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Тестовый клиент для отправки запросов"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """CLI-клиент (для команд вроде flask db)"""
    return app.test_cli_runner()


@pytest.fixture
def empty_db(app):
    """Фикстура для тестов, которым нужна чистая БД без данных"""
    with app.app_context():
        # Очищаем все таблицы
        db.session.remove()
        db.drop_all()
        db.create_all()
    yield


@pytest.fixture
def init_database(app):
    """Фикстура: добавляет тестовые данные (категории и вопросы)"""
    with app.app_context():
        from app.models import Category, Question

        # Очищаем БД перед добавлением
        db.session.remove()
        db.drop_all()
        db.create_all()

        # Создаём категории
        science = Category(name="Science")
        history = Category(name="History")
        programming = Category(name="Programming")
        db.session.add_all([science, history, programming])
        db.session.commit()

        # Сохраняем ID для использования в тестах
        science_id = science.id
        history_id = history.id
        programming_id = programming.id

        # Создаём вопросы
        q1 = Question(text="What is H2O?", answer="Water", category_id=science.id)
        q2 = Question(text="Capital of France?", answer="Paris", category_id=history.id)
        q3 = Question(text="What is Python?", answer="Programming language", category_id=programming.id)
        db.session.add_all([q1, q2, q3])
        db.session.commit()

    # Возвращаем ID для использования в тестах
    yield {
        'science_id': science_id,
        'history_id': history_id,
        'programming_id': programming_id
    }