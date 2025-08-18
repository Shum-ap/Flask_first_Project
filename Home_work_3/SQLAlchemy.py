from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship

# 🔹 Создаём движок SQLite в памяти
engine = create_engine("sqlite:///:memory:", echo=False)

# 🔹 Базовый класс для декларативного маппинга
class Base(DeclarativeBase):
    pass

# 🔹 Модель Category
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category(name='{self.name}')>"

# 🔹 Модель Product
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)
    category = relationship("Category", back_populates="products")

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price}, in_stock={self.in_stock})>"

# 🔹 Создаём таблицы
Base.metadata.create_all(engine)

# 🔹 Создаём сессию
Session = sessionmaker(bind=engine)
session = Session()

# --- Добавляем 5 категорий и продукты ---
categories = [
    Category(name="Электроника", description="Гаджеты и устройства"),
    Category(name="Книги", description="Разные жанры"),
    Category(name="Одежда", description="Для мужчин и женщин"),
    Category(name="Продукты питания", description="Еда и напитки"),
    Category(name="Спорт и отдых", description="Спортивные товары и отдых")
]

products = [
    Product(name="Ноутбук", price=75999.99, in_stock=True, category=categories[0]),
    Product(name="Смартфон", price=49999.50, in_stock=True, category=categories[0]),
    Product(name="Футболка", price=1200.00, in_stock=False, category=categories[2]),
    Product(name="Книга Python", price=1500.00, in_stock=True, category=categories[1]),
    Product(name="Беговые кроссовки", price=8500.00, in_stock=True, category=categories[4])
]

session.add_all(categories + products)
session.commit()

# --- Вывод продуктов по категориям ---
for c in session.query(Category).all():
    print(f"Категория: {c.name} ({c.description})")
    if c.products:
        for p in c.products:
            status = "Да" if p.in_stock else "Нет"
            print(f"  - {p.name}, цена: {p.price} ₽, в наличии: {status}")
    else:
        print("  (Нет продуктов)")
    print()

# 🔚 Закрываем сессию
session.close()