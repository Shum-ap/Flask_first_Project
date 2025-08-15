from pydantic import BaseModel, Field, EmailStr, ValidationError, model_validator, field_validator
import json

class Address(BaseModel):
    city: str = Field(..., min_length=2 ,description="City name")
    street: str = Field(..., min_length=3, description="Street name")
    house_number: int = Field(..., gt=0 , description="Haus nummer, positive integer nummer")

class User(BaseModel):
    name: str = Field(...,  redex=r'^[a-zA-Z- ]{2,50}$' ,description="User name")
    age: int = Field(..., ge=0, le=120, description="Age")
    email: EmailStr = Field(..., description="Email adress")
    is_employed: bool = Field (default=True, description="Whether user is employed")
    address: Address

    @model_validator(mode='after')
    def check_employment_age(cls, values):
        age = values.age
        employed = values.is_employed
        if employed and not (18 <= age <= 65):
            raise ValueError('Employed users must be between 18 and 65 years old')
        return values

    @field_validator('name')
    def name_must_be_letters(cls, v):
        if not all(x.isalpha() or x.isspace() for x in v):
            raise ValueError('Name must contain only letters and spaces')
        return v

def register_user(json_str: str):
    try:
        data = json.loads(json_str)
        user = User.model_validate(data)
        print("=== Successful Registration ===")
        print(user.model_dump_json(indent=4))
    except ValidationError as e:
        print("=== Validation Error ===")
        for err in e.errors():
            loc = ' -> '.join(str(x) for x in err['loc'])
            msg = err['msg']
            val = err.get('input', None)
            print(f"Field: {loc}\n  Value: {val}\n  Error: {msg}\n")

# Примеры
json_success = """{
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
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

register_user(json_success)
register_user(json_age_error)
register_user(json_email_error)
