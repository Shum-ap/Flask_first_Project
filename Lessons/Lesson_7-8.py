from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, ForeignKey, Numeric, func, desc
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, aliased
from datetime import datetime, timedelta

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)

# 1. Create engine (using SQLite in-memory DB for demo)
engine = create_engine("sqlite:///:memory:", echo=True)

# 2. Create tables
Base.metadata.create_all(engine)

# 3. Create session
Session = sessionmaker(bind=engine)
session = Session()

# 4. Insert rows
session.add_all(
    [
        User(name="Bob", age=22),
        User(name="David", age=27),
        User(name="Alice", age=30),
        User(name="Ann", age=17),
        User(name="Ann", age=27),
    ]
)

# 5. Commit changes
session.commit()

# 6. Query back
for user in session.query(User).all():
    print(user.id, user.name, user.age)


# Поиск пользователей, чье имя начинается на "A"
users = session.query(User).filter(User.name.like("A%")).all()
print("Имена начинаются на 'A':")
for user in users:
    print(user.id, user.name)

# Поиск пользователей с ID между 2 и 4
users = session.query(User).filter(User.id.between(2, 4)).all()
print("\nID между 2 и 4:")
for user in users:
    print(user.id, user.name)

# Поиск пользователей, чьи имена находятся в списке
names = ["Alice", "Bob"]
users = session.query(User).filter(User.name.in_(names)).all()
print("\nИмена из списка [Alice, Bob]:")
for user in users:
    print(user.id, user.name)


from sqlalchemy import and_, or_, not_

# Выборка пользователей старше 20 лет и младше 23 лет
users = session.query(User).filter(and_(User.age > 20, User.age < 23)).all()
print("Пользователи старше 20 и младше 23:")
for user in users:
    print(user.id, user.name, user.age)

# Выборка пользователей старше 30 или с именем David
users = session.query(User).filter(or_(User.age > 30, User.name == 'David')).all()
print("\nПользователи старше 30 или с именем David:")
for user in users:
    print(user.id, user.name, user.age)

# Выборка пользователей не с именем David
users = session.query(User).filter(not_(User.name == 'David')).all()
print("\nПользователи, не с именем David:")
for user in users:
    print(user.id, user.name, user.age)


from sqlalchemy import desc

# Сортировка пользователей по возрасту от меньшего к большему
users = session.query(User).order_by(User.age).all()
print("Сортировка по возрасту (по возрастанию):")
for user in users:
    print(user.id, user.name, user.age)

# Сортировка пользователей по возрасту от большего к меньшему
users = session.query(User).order_by(desc(User.age)).all()
print("\nСортировка по возрасту (по убыванию):")
for user in users:
    print(user.id, user.name, user.age)

# Сортировка пользователей по возрасту от большего к меньшему и по имени по алфавиту
users = session.query(User).order_by(desc(User.age), User.name).all()
print("\nСортировка по возрасту (по убыванию) и имени (по алфавиту):")
for user in users:
    print(user.id, user.name, user.age)




# Суммирование возрастов пользователей, группировка по именам
total_ages = session.query(User.name, func.sum(User.age)).group_by(User.name).all()
print("Сумма возрастов по именам:")
for name, total_age in total_ages:
    print(f"{name}: {total_age}")

# Подсчет количества пользователей в каждой возрастной группе
age_groups = session.query(User.age, func.count(User.id)).group_by(User.age).all()
print("\nКоличество пользователей по возрасту:")
for age, count in age_groups:
    print(f"{age} лет: {count} человек")

# Подсчет общего количества пользователей в таблице
total_count = session.query(func.count(User.id)).scalar()
print("Users count:", total_count)



# Создаем алиас для таблицы User
user_alias = aliased(User, name='user_alias')

# Присвоение алиаса выражению подсчета количества пользователей в каждой возрастной группе
age_groups = session.query(
    user_alias.age,
    func.count(user_alias.id).label('total_users')
).group_by(user_alias.age).all()

# Теперь можно обращаться к присвоенному имени 'total_users'
print("Количество пользователей по возрасту (с использованием алиаса):")
for group in age_groups:
    print(group.age, group.total_users)


# Подсчет количества пользователей в каждой возрастной группе
# и исключение групп с количеством меньше двух
age_groups = session.query(
    User.age,
    func.count(User.id).label('count_users')
).group_by(User.age).having(func.count(User.id) > 1).all()

print("Возрастные группы с количеством пользователей > 1:")
for age, count in age_groups:
    print(f"{age} лет: {count} человек")


# Подзапрос для вычисления среднего возраста
average_age_subquery = session.query(func.avg(User.age).label('average_age')).subquery()

# Основной запрос, использующий подзапрос для фильтрации пользователей
users = session.query(User).filter(User.age > average_age_subquery.c.average_age).all()

# Выполним подзапрос отдельно для проверки результата
average_age = session.query(func.avg(User.age)).scalar()
print(f"Average age is {average_age:.2f}")

# Выведем отобранные данные
print("\nПользователи старше среднего возраста:")
for user in users:
    print(user.id, user.name, user.age)




# Создание связанной таблицы
class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String)

    # Связь с таблицей User
    user = relationship("User", back_populates="addresses")

# Добавляем связь в User
User.addresses = relationship("Address", order_by=Address.id, back_populates="user")

# Создание таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Заполнение таблицы адресами
session.add_all([
    Address(user_id=1, description='New York'),
    Address(user_id=2, description='London'),
    Address(user_id=4, description='Berlin')
])
session.commit()


# Присоединение таблицы адресов к таблице пользователей с помощью Inner Join
users = session.query(User).join(Address).all()

# Проверка выборки
for user in users:
    print(user.id, user.name, user.age)
    for address in user.addresses:
        print("Address:", address.id, address.description)



# Присоединение таблицы адресов к таблице пользователей с помощью Left Outer Join
users = session.query(User).outerjoin(Address).all()

# Проверка выборки
for user in users:
    print(user.id, user.name, user.age)
    for address in user.addresses:
        print("Address:", address.id, address.description)




Base = declarative_base()
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()

# Определение классов
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    orders = relationship("Order", back_populates="user")
    addresses = relationship("Address", back_populates="user")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Numeric)
    created_at = Column(DateTime)
    user = relationship("User", back_populates="orders")

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String)
    user = relationship("User", back_populates="addresses")

Base.metadata.create_all(engine)

# Добавление пользователей
user1 = User(name="Alice", age=30)
user2 = User(name="Bob", age=22)
session.add_all([user1, user2])
session.commit()

# Добавление заказов
order1 = Order(user_id=user1.id, amount=100.50, created_at=datetime.now() - timedelta(days=1))
order2 = Order(user_id=user1.id, amount=200.75, created_at=datetime.now())
order3 = Order(user_id=user2.id, amount=80.99, created_at=datetime.now() - timedelta(days=2))
session.add_all([order1, order2, order3])
session.commit()

# Добавление адресов
address1 = Address(user_id=user1.id, description='New York')
address2 = Address(user_id=user2.id, description='New York')  # тот же город, что и user1
session.add_all([address1, address2])
session.commit()

# Найти всех пользователей, которые живут в одном городе с другими
address_alias1 = aliased(Address)
address_alias2 = aliased(Address)

users_same_city = session.query(address_alias1.user_id, address_alias2.user_id)\
    .join(address_alias2, address_alias1.description == address_alias2.description)\
    .filter(address_alias1.user_id != address_alias2.user_id).all()

print("Пользователи в одном городе с другими:", users_same_city)

# Подзапрос для определения последнего заказа каждого пользователя
subquery = session.query(
    Order.user_id,
    func.max(Order.created_at).label('last_order_time')
).group_by(Order.user_id).subquery()

# Основной запрос: пользователи, их последние заказы и сумма
complex_query = session.query(
    User.name,
    User.age,
    func.round(Order.amount, 2).label('amount'),
    subquery.c.last_order_time
).join(User.orders)\
 .join(subquery, User.id == subquery.c.user_id)\
 .filter(Order.created_at == subquery.c.last_order_time)\
 .order_by(User.name, desc(Order.amount))

print("\nПоследние заказы пользователей:")
for result in complex_query.all():
    print(result)
