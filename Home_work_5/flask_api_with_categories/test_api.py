import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def safe_post(url, data):
    resp = requests.post(url, json=data)
    if resp.status_code not in (200, 201):
        print(f"Ошибка {resp.status_code} при POST {url}: {resp.text}")
        return None
    return resp.json()

def safe_get(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"Ошибка {resp.status_code} при GET {url}: {resp.text}")
        return None
    return resp.json()

def pretty_print(title, data):
    print(f"\n=== {title} ===")
    if data is not None:
        print(json.dumps(data, ensure_ascii=False, indent=2))

# Создаём категории
categories = ["Программирование", "Математика"]
created_categories = []
for name in categories:
    created_categories.append(safe_post(f"{BASE_URL}/categories", {"name": name}))
pretty_print("Созданные категории", created_categories)

# Получаем все категории
all_categories = safe_get(f"{BASE_URL}/categories")
pretty_print("Все категории", all_categories)

# Создаём вопросы (используем ключ "text" как требует сервер)
questions = [
    {"text": "Что такое Python?", "category_id": 1},
    {"text": "Что такое интеграл?", "category_id": 2}
]
created_questions = []
for q in questions:
    created_questions.append(safe_post(f"{BASE_URL}/questions", q))
pretty_print("Созданные вопросы", created_questions)

# Получаем все вопросы
all_questions = safe_get(f"{BASE_URL}/questions")
pretty_print("Все вопросы", all_questions)
