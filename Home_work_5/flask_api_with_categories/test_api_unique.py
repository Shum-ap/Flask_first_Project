import requests
import json
import time

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

# Уникальные имена категорий и вопросов с помощью времени
timestamp = int(time.time())
categories = [f"Категория {timestamp}", f"Категория {timestamp+1}"]
questions = [
    {"text": f"Вопрос по Python {timestamp}", "category_index": 0},
    {"text": f"Вопрос по математике {timestamp}", "category_index": 1}
]

# Создаём категории
created_categories = []
for name in categories:
    created_categories.append(safe_post(f"{BASE_URL}/categories", {"name": name}))
pretty_print("Созданные категории", created_categories)

# Получаем актуальные категории из базы
all_categories = safe_get(f"{BASE_URL}/categories")
pretty_print("Все категории", all_categories)

# Создаём вопросы с правильными category_id
created_questions = []
for q in questions:
    category_id = created_categories[q["category_index"]]["id"] if created_categories[q["category_index"]] else all_categories[q["category_index"]]["id"]
    created_questions.append(safe_post(f"{BASE_URL}/questions", {"text": q["text"], "category_id": category_id}))
pretty_print("Созданные вопросы", created_questions)

# Получаем все вопросы
all_questions = safe_get(f"{BASE_URL}/questions")
pretty_print("Все вопросы", all_questions)
