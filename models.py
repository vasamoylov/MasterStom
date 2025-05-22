from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint

Base = declarative_base()


class Clients(Base):
    __tablename__ = 'clients'
    # Таблица с личными данными клиентов

    __table_args__ = (
        CheckConstraint('age > 0', name='check_age'),
    )
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), nullable=False, index=True)
    surname = Column(String(25))
    patronymic = Column(String(25))
    age = Column(Integer)
    phone = Column(String(15), nullable=False, unique=True)
    email = Column(String(20))
    client_subscriptions = relationship('ClientSubscriptions', back_populates='client')
    services_availability = relationship('ServicesAvailability', back_populates='client')


class Subscriptions(Base):
    __tablename__ = 'subscriptions'
    # Таблица с наименованием подписок

    __table_args__ = (
        CheckConstraint('price > 0', name='check_price'),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    price = Column(Integer, nullable=False)
    client_subscriptions = relationship('ClientSubscriptions', back_populates='subscription')
    services = relationship('Services', back_populates='subscription')


class ClientSubscriptions(Base):
    __tablename__ = 'client_subscriptions'
    # Таблица с информацией о подписках клиентов

    __table_args__ = (
        CheckConstraint('start_date < end_date', name='check_date'),
    )
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    payment_status = Column(String(10), nullable=False)
    client = relationship('Clients', back_populates='client_subscriptions')
    subscription = relationship('Subscriptions', back_populates='client_subscriptions')


class Services(Base):
    __tablename__ = 'services'
    # Таблица с перечнем услуг и ценами, которые входят в подписки

    __table_args__ = (
        CheckConstraint('price > 0', name='check_price'),
    )
    id = Column(Integer, primary_key=True)
    id_subscription = Column(Integer, ForeignKey('subscriptions.id'))
    description = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    services_availability = relationship('ServicesAvailability', back_populates='service')
    subscription = relationship('Subscriptions', back_populates='services')


class ServicesAvailability(Base):
    __tablename__ = 'services_availability'
    # Таблица с информацией о количестве доступных улуг для клиента в рамках подписки

    __table_args__ = (
        CheckConstraint('quantity >= 0', name='check_quantitye'),
    )
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    service_id = Column(Integer, ForeignKey('services.id'))
    quantity = Column(Integer, nullable=False)
    client = relationship('Clients', back_populates='services_availability')
    service = relationship('Services', back_populates='services_availability')


class Contacts(Base):
    __tablename__ = 'contacts'
    # Таблица с контактами

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    url = Column(String(30), nullable=False)


class Offers(Base):
    __tablename__ = 'offers'
    # Таблица с оферами

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    url = Column(String(30), nullable=False)


class Categories(Base):
    __tablename__ = 'categories'
    # Таблица с категориями стоматологических услуг (ортопедия, хирургия и т.п.)

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    service = relationship('PriceList', back_populates='category')


class PriceList(Base):
    __tablename__ = 'price_list'
    # Прайс лист всех стоматологических услуг

    __table_args__ = (
        CheckConstraint('price > 0', name='check_price'),
    )
    id = Column(Integer, primary_key=True)
    category_id = Column(String(10), ForeignKey('categories.id'))
    description = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    category = relationship('Categories', back_populates='service')

