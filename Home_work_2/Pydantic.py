from pydantic import BaseModel, Field, EmailStr, ValidationError, model_validator, field_validator
import json

class Address(BaseModel):
    city: str = Field(..., min_length=2, description="Название города")
    street: str = Field(..., min_length=3, description="Название улицы")
    house_number: int = Field(..., gt=0, description="Номер дома, положительное число")

class User(BaseModel):
    name: str = Field(
        ...,
        pattern=r'^[A-Za-zА-Яа-яЁё]+(?:[ -][A-Za-zА-Яа-яЁё]+)*$',
        description="Имя пользователя (латиница или кириллица, пробелы и дефисы допустимы внутри)"
    )
    age: int = Field(..., ge=0, le=120, description="Возраст")
    email: EmailStr = Field(..., description="Электронная почта")
    is_employed: bool = Field(default=True, description="Занят ли пользователь")
    address: Address

    @model_validator(mode='after')
    def check_employment_age(cls, user):
        if user.is_employed and not (18 <= user.age <= 65):
            raise ValueError('Работающие пользователи должны быть в возрасте от 18 до 65 лет')
        return user

    @field_validator('name')
    def name_must_be_letters(cls, v):
        # Дополнительная проверка на символы (для надёжности)
        if not all(x.isalpha() or x in " - " for x in v):
            raise ValueError('Имя должно содержать только буквы, пробелы и дефисы')
        return v

def register_user(json_str: str):
    try:
        data = json.loads(json_str)
        user = User.model_validate(data)
        print("=== Регистрация успешна ===")
        print(user.model_dump_json(indent=4))
    except ValidationError as e:
        print("=== Ошибка валидации ===")
        for err in e.errors():
            loc = ' -> '.join(str(x) for x in err['loc'])
            msg = err['msg']
            val = err.get('input', None)
            print(f"Поле: {loc}\n  Значение: {val}\n  Ошибка: {msg}\n")

# Примеры JSON
json_success = """{
    "name": "Иван Иванов",
    "age": 30,
    "email": "ivan.ivanov@example.com",
    "is_employed": true,
    "address": {
        "city": "Москва",
        "street": "Тверская",
        "house_number": 15
    }
}"""

json_age_error = """{
    "name": "Jane Smith",
    "age": 70,
    "email": "jane.smith@example.com",
    "is_employed": true,
    "address": {
        "city": "Los Angeles",
        "street": "Sunset Blvd",
        "house_number": 45
    }
}"""

json_email_error = """{
    "name": "Alice",
    "age": 25,
    "email": "alice[at]example.com",
    "is_employed": false,
    "address": {
        "city": "Boston",
        "street": "Main St",
        "house_number": 10
    }
}"""

# Проверка
register_user(json_success)
register_user(json_age_error)
register_user(json_email_error)
