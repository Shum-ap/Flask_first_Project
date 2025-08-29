# app/schemas/question.py
from pydantic import BaseModel, ConfigDict
from typing import Optional


class CategoryBase(BaseModel):
    id: Optional[int] = None
    name: str

    model_config = ConfigDict(from_attributes=True)


class QuestionBase(BaseModel):
    id: Optional[int] = None
    text: str
    answer: str
    category_id: Optional[int] = None
    category: Optional[CategoryBase] = None

    model_config = ConfigDict(from_attributes=True)


class QuestionCreate(QuestionBase):
    text: str
    answer: str
    category_id: Optional[int] = None


class QuestionResponse(QuestionBase):
    pass