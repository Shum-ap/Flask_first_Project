# from sqlalchemy import create_engine
# # PostgreSQL
# engine = create_engine('postgresql://user:password@localhost:5432/mydatabase')
# # MySQL
# engine = create_engine('mysql+pymysql://user:password@localhost:3306/mydatabase')
# # SQLite (для локального файла)
# engine = create_engine('sqlite:///path/to/database.db')
# # SQLite (в оперативной памяти)
# engine = create_engine('sqlite:///:memory:')
#
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import sessionmaker, declarative_base
# Base = declarative_base()
# engine = create_engine('sqlite:///example.db')
# # Определяем класс `User`, который наследуется от базового класса `Base`.
# # Этот класс представляет собой сущность базы данных.
# class User(Base):
# __tablename__ = 'users'
# id = Column(Integer, primary_key=True)
# name = Column(String(30))
# age = Column(Integer)
# Session = sessionmaker(bind=engine)
# session = Session()
# # Для того чтобы в базе данных появилась таблицы вызываем метод
# `create_all()` объекта `metadata` базового класса `Base`
# # SQLAlchemy автоматически анализирует классы моделей данных и создает
# соответствующие таблицы в базе данных.
# Base.metadata.create_all(engine)
# # Создание нового пользователя
# new_user = User(name="John Doe", age=30)
# # Добавляем объект в сессию с помощью метода `add()`.
# session.add(new_user)

from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship

# 🔹 Задача 1: движок SQLite в памяти
engine = create_engine("sqlite:///:memory:", echo=True)

# 🔹 Базовый класс
class Base(DeclarativeBase):
    pass

# 🔹 Задача 4: модель Category
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    products = relationship("Product", back_populates="category")

# 🔹 Задача 3: модель Product
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")

# 🔹 Создаём таблицы
Base.metadata.create_all(engine)

# 🔹 Задача 2: создаём сессию
Session = sessionmaker(bind=engine)
session = Session()
