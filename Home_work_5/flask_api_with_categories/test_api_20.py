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

# Создаём уникальные категории
timestamp = int(time.time())
categories = [f"Категория {timestamp + i}" for i in range(10)]

created_categories = []
for name in categories:
    created_categories.append(safe_post(f"{BASE_URL}/categories", {"name": name}))
pretty_print("Созданные категории", created_categories)

# Получаем актуальные категории из базы
all_categories = safe_get(f"{BASE_URL}/categories")
pretty_print("Все категории", all_categories)

# Создаём 20 вопросов, по 2 на каждую категорию
created_questions = []
for i in range(20):
    category_index = i % len(created_categories)
    category_id = created_categories[category_index]["id"] if created_categories[category_index] else all_categories[category_index]["id"]
    question_text = f"Вопрос {i+1} для {categories[category_index]}"
    created_questions.append(safe_post(f"{BASE_URL}/questions", {"text": question_text, "category_id": category_id}))

pretty_print("Созданные вопросы", created_questions)

# Получаем все вопросы
all_questions = safe_get(f"{BASE_URL}/questions")
pretty_print("Все вопросы", all_questions)
