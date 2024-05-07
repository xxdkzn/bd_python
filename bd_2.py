from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Подключение к базе данных PostgreSQL
engine = create_engine('postgresql://username:password@localhost:5432/bd_name')
Session = sessionmaker(bind=engine)
session = Session()

# Определение моделей данных
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    publisher = relationship('Publisher', back_populates='books')
    purchases = relationship('Purchase', back_populates='book')

class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship('Book', back_populates='publisher')

class Purchase(Base):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship('Book', back_populates='purchases')
    store_id = Column(Integer, ForeignKey('stores.id'))
    store = relationship('Store', back_populates='purchases')
    price = Column(Integer)
    purchase_date = Column(DateTime)

class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    purchases = relationship('Purchase', back_populates='store')

# Запрос на выборку магазинов, продающих целевого издателя
def get_stores_by_publisher(publisher_name):
    publisher = session.query(Publisher).filter(Publisher.name == publisher_name).first()
    if publisher:
        purchases = session.query(Purchase).\
                     join(Purchase.book).\
                     filter(Book.publisher_id == publisher.id).\
                     join(Purchase.store).\
                     all()
        for purchase in purchases:
            print(f"{purchase.book.title} | {purchase.store.name} | {purchase.price} | {purchase.purchase_date.strftime('%d-%m-%Y')}")
    else:
        print(f"Издатель с именем '{publisher_name}' не найден.")

# Пример использования
publisher_name = input("Введите имя или ID издателя: ")
get_stores_by_publisher(publisher_name)