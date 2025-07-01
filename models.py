from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint, Enum

Base = declarative_base()


class Clients(Base):
    __tablename__ = 'clients'
    '''Таблица с личными данными клиентов'''

    __table_args__ = (
        CheckConstraint('age > 0', name='check_age'),
    )
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), nullable=False, index=True)
    surname = Column(String(25))
    patronymic = Column(String(25))
    age = Column(Integer)
    phone = Column(String(15), nullable=False, unique=True, index=True)
    email = Column(String(50))
    client_subscription = relationship('ClientSubscriptions', back_populates='client',
                                       cascade='all, delete-orphan')
    services_availability = relationship('ServicesAvailability', back_populates='client',
                                         cascade='all, delete-orphan')


class Subscriptions(Base):
    __tablename__ = 'subscriptions'
    '''Таблица с наименованием подписок'''

    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price'),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    price = Column(Integer, nullable=False)
    client_subscription = relationship('ClientSubscriptions', back_populates='subscription',
                                       cascade='all, delete-orphan')
    included_services = relationship('Services', back_populates='subscriptions')


class ClientSubscriptions(Base):
    __tablename__ = 'client_subscriptions'
    '''Таблица с информацией о подписках клиентов'''

    __table_args__ = (
        CheckConstraint('start_date < end_date', name='check_date'),
    )
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    payment_status = Column(Enum('paid', 'not_paid'))
    client = relationship('Clients', back_populates='client_subscription')
    subscription = relationship('Subscriptions', back_populates='client_subscription')


class Categories(Base):
    __tablename__ = 'categories'
    '''Таблица с категориями стоматологических услуг (ортопедия, хирургия и т.п.)'''

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    services = relationship('Services', back_populates='category',
                            cascade='all, delete-orphan')


class Services(Base):
    __tablename__ = 'services'
    '''Таблица с перечнем услуг и ценами, в т.ч. которые входят в подписки'''

    __table_args__ = (
        CheckConstraint('price > 0', name='check_price'),
        CheckConstraint('price > 0', name='check_price'),
    )
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    description = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))
    quantity = Column(Integer)
    services_availability = relationship('ServicesAvailability', back_populates='service')
    subscriptions = relationship('Subscriptions', back_populates='included_services')
    category = relationship('Categories', back_populates='services')


class ServicesAvailability(Base):
    __tablename__ = 'services_availability'
    '''Таблица с информацией о количестве доступных улуг для клиента в рамках подписки'''

    __table_args__ = (
        CheckConstraint('quantity >= 0', name='check_quantity'),
    )
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    service_id = Column(Integer, ForeignKey('services.id'))
    quantity = Column(Integer, nullable=False)
    client = relationship('Clients', back_populates='services_availability')
    service = relationship('Services', back_populates='services_availability')


class Contacts(Base):
    __tablename__ = 'contacts'
    '''Таблица с контактами клиники'''

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    url = Column(String(30), nullable=False)


class Offers(Base):
    __tablename__ = 'offers'
    '''Таблица с оферами'''

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    url = Column(String(30), nullable=False)

