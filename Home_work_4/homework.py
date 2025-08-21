from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Создаем базу данных в пам:
Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Определяем таблицы:
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")

# Создаем таблицы в базе:
Base.metadata.create_all(engine)

# Задача 1: Наполнение данными:

# Добавление категорий:
electronics = Category(name="Электроника", description="Гаджеты и устройства.")
books = Category(name="Книги", description="Печатные книги и электронные книги.")
clothing = Category(name="Одежда", description="Одежда для мужчин и женщин.")

session.add_all([electronics, books, clothing])
session.commit()

# Добавление продуктов:
products = [
    Product(name="Смартфон", price=299.99, in_stock=True, category=electronics),
    Product(name="Ноутбук", price=499.99, in_stock=True, category=electronics),
    Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=books),
    Product(name="Джинсы", price=40.50, in_stock=True, category=clothing),
    Product(name="Футболка", price=20.00, in_stock=True, category=clothing)
]

session.add_all(products)
session.commit()

# Задача 2: Чтение данных:
print("\nКатегории и их продукты:")
categories = session.query(Category).all()
for cat in categories:
    print(f"Категория: {cat.name}")
    for prod in cat.products:
        print(f"  Продукт: {prod.name}, Цена: {prod.price}")

# Задача 3: Обновление данных:
smartphone = session.query(Product).filter_by(name="Смартфон").first()
if smartphone:
    smartphone.price = 349.99
    session.commit()
    print(f"\nЦена продукта '{smartphone.name}' обновлена на {smartphone.price}")

# Задача 4: Агрегация и группировка:
print("\nКоличество продуктов в каждой категории:")
counts = session.query(
    Category.name,
    func.count(Product.id).label('total_products')
).join(Product).group_by(Category.id).all()

for name, total in counts:
    print(f"{name}: {total} продукта(ов)")

#5: Группировка с фильтрацией:
print("\nКатегории с более чем одним продуктом:")
filtered = session.query(
    Category.name,
    func.count(Product.id).label('total_products')
).join(Product).group_by(Category.id).having(func.count(Product.id) > 1).all()

for name, total in filtered:
    print(f"{name}: {total} продукта(ов)")
