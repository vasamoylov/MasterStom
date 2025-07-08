from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import List
from sqlalchemy import create_engine, insert, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker, Session
from models import Base, Clients, Subscriptions, Services, ClientSubscriptions, ServicesAvailability, Categories
from datetime import date

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


class ClientCreate(BaseModel):
    name: str
    surname: str
    patronymic: str
    age: int
    phone: PhoneNumber
    email: EmailStr


class SubscriptionCreate(BaseModel):
    name: str
    price: int


class CategoryCreate(BaseModel):
    name: str


class ServiceCreate(BaseModel):
    category_id: int
    description: str
    price: int
    subscription_id: int
    quantity: int


class ClientSubscriptionCreate(BaseModel):
    client_id: int
    subscription_id: int
    start_date: date
    end_date: date
    payment_status: str


class ClientResponse(ClientCreate):
    id: int


class SubscriptionResponse(SubscriptionCreate):
    id: int


class CategoryResponse(CategoryCreate):
    id: int


class ServiceResponse(ServiceCreate):
    id: int


app = FastAPI(
    title='MasterStom Clients',
    description='Clients and Subscriptoins'
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/clients/', response_model=ClientResponse)
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = Clients(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@app.get('/clients/')
async def get_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    total_clients = db.query(Clients).count()
    clients = db.query(Clients).offset(skip).limit(limit).all()
    return {
        'total': total_clients,
        'skip': skip,
        'limit': limit,
        'clients': clients
    }


@app.get('/clients/{id}', response_model=ClientResponse)
async def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.get(Clients, client_id)
    if not client:
        raise HTTPException(status_code=404, detail='Client not found')
    return client


@app.put('/clients/{id}', response_model=ClientResponse)
async def update_client(client_id: int, client: ClientCreate, db: Session = Depends(get_db)):
    db_client = db.get(Clients, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail='Client not found')
    db_client.name = client.name
    db_client.surname = client.surname
    db_client.patronymic = client.patronymic
    db_client.age = client.age
    db_client.phone = client.phone
    db_client.email = client.email
    db.commit()
    db.refresh(db_client)
    return db_client


@app.delete('/clients/{id}')
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.get(Clients, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail='Client not found')
    db.delete(db_client)
    db.commit()
    return {'message': 'Client deleted'}


@app.get('/clients/services/')
async def get_price_list(db: Session = Depends(get_db)):
    price_list = db.query(Services.description, Services.price).distinct().all()
    return price_list


@app.post('/subscriptions/', response_model=SubscriptionResponse)
async def create_subscription(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    db_subscription = Subscriptions(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


@app.get('/subscriptions/')
async def get_subscriptions(db: Session = Depends(get_db)):
    subscriptions = db.query(Subscriptions).all()
    return subscriptions


@app.put('/subscriptions/{id}', response_model=SubscriptionResponse)
async def get_subscription(subscription_id, subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    db_subscription = db.get(Subscriptions, subscription_id)
    if not db_subscription:
        raise HTTPException(status_code=404, detail='Subscription not found')
    db_subscription.name = subscription.name
    db_subscription.price = subscription.price
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


@app.delete('/subscriptions/{id}')
async def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    db_subscription = db.get(Subscriptions, subscription_id)
    if not db_subscription:
        raise HTTPException(status_code=404, detail='Subscription not found')
    db.delete(db_subscription)
    db.commit()
    return {'message': 'Subscription deleted'}


@app.post('/categories/', response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Categories(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.get('/categories/')
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Categories).all()
    return categories


@app.put('/categories/{id}', response_model=CategoryResponse)
async def get_category(category_id, category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.get(Categories, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail='Category not found')
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category


@app.delete('/categories/{id}')
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.get(Categories, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail='Categoryn not found')
    db.delete(db_category)
    db.commit()
    return {'message': 'Category deleted'}


@app.post('/services/', response_model=ServiceResponse)
async def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    db_service = Services(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


@app.get('/services/')
async def get_services(db: Session = Depends(get_db)):
    services = db.query(Services).all()
    return services


@app.put('/services/{id}', response_model=ServiceResponse)
async def get_service(service_id, service: ServiceCreate, db: Session = Depends(get_db)):
    db_service = db.get(Services, service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail='Service not found')
    db_service.category_id = service.category_id
    db_service.description = service.description
    db_service.price = service.price
    db_service.subscription_id = service.subscription_id
    db_service.quantity = service.quantity
    db.commit()
    db.refresh(db_service)
    return db_service


@app.delete('/services/{id}')
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    db_service = db.get(Services, service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail='Service not found')
    db.delete(db_service)
    db.commit()
    return {'message': 'Service deleted'}


@app.post('/clients/{id}/subscription/')
async def create_client_subscription(client_subscription: ClientSubscriptionCreate, db: Session = Depends(get_db)):
    db_client_subscription = ClientSubscriptions(**client_subscription.dict())
    db.add(db_client_subscription)
    service_availability = (
        db.query(
            Services.id, Services.quantity).filter_by(subscription_id=db_client_subscription.subscription_id).all()
    )
    for service in service_availability:
        db_service = ServicesAvailability(db_client_subscription.client_id, service.id, service.quantity)
        db.add(db_service)
    db.commit()
    db.refresh(db_client_subscription)
    return {'message': 'Subscription completed successfully'}


@app.get('/clients/{id}/subscription/')
async def get_client_subscription(client_id: int, db: Session = Depends(get_db)):
    client = db.get(ClientSubscriptions, client_id)
    if not client:
        raise HTTPException(status_code=404, detail='Client not have subscription')
    else:
        client_subscription = db.query(ClientSubscriptions).filter_by(client_id=client_id).one()
    return client_subscription


@app.put('/clients/{id}/subscription/', response_model=ClientResponse)
async def update_client_subscription(client_id: int, client_subscription: ClientSubscriptionCreate,
                                     db: Session = Depends(get_db)):
    db_client = db.get(ClientSubscriptions, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail='Client not found')
    db_client.subscription_id = client_subscription.subscription_id
    db.commit()
    db.refresh(db_client)
    return db_client


@app.delete('/clients/{id}/subscription/')
async def delete_client_subscription(client_subscription_id: int, db: Session = Depends(get_db)):
    db_client_subscription = db.get(ClientSubscriptions, client_subscription_id)
    if not db_client_subscription:
        raise HTTPException(status_code=404, detail='Client subscription not found')
    db.delete(db_client_subscription)
    db.commit()
    return {'message': 'Client subscription deleted'}


@app.put('/clients/{id}/subscription/services/')
async def use_availability_services(client_id: int, service_id: int, quantity: int, db: Session = Depends(get_db)):
    db_availability_quantity = (
        db.query(ServicesAvailability.quantity).filter_by(client_id=client_id, service_id=service_id)).one()
    print(db_availability_quantity)
    print(quantity)
    if not db_availability_quantity:
        raise HTTPException(status_code=404, detail='This service is not included in the subscription')
    print('if not db_availability_quantity')
    print(db_availability_quantity.quantity, quantity)
    db_availability_quantity.quantity = db_availability_quantity.quantity - quantity
    print(db_availability_quantity.quantity, quantity)
    db.commit()
    return {'message': 'The service was successfully used'}


# from sqlalchemy import MetaData

# metadata = MetaData()
# metadata.reflect(bind=engine)
# my_table = metadata.tables['alembic_version']
# my_table.drop(engine)


session = Session(bind=engine)
data = session.query(ServicesAvailability.service_id, ServicesAvailability.quantity).filter_by(client_id=1).all()
new_data = session.query(Services.id, Services.quantity).filter_by(subscription_id=2).all()

print(data)
print(new_data)


