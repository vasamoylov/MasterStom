from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from models import Base, Clients, Subscriptions, Services

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


class ServiceCreate(BaseModel):
    id_subscription: int
    description: str
    price: int


class ClientResponse(ClientCreate):
    id: int


class SubscriptionResponse(SubscriptionCreate):
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


@app.get('/clients/', response_model=List[ClientResponse])
async def get_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clients = db.query(Clients).offset(skip).limit(limit).all()
    return clients


@app.get('/clients/{id}', response_model=ClientResponse)
async def get_contact(client_id: int, db: Session = Depends(get_db)):
    client = db.get(Clients, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Contact not found")
    return client


@app.put('/clients/{id}', response_model=ClientResponse)
async def update_contact(contact_id: int, client: ClientCreate, db: Session = Depends(get_db)):
    db_client = db.get(Clients, contact_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Contact not found")
    db_client.name = client.name
    db.commit()
    db.refresh(db_client)
    return db_client


@app.delete('/contacts/{id}')
async def delete_contact(client_id: int, db: Session = Depends(get_db)):
    db_client = db.get(Clients, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_client)
    db.commit()
    return {"message": "Contact deleted"}


@app.post('/subscriptions/', response_model=SubscriptionResponse)
async def create_subscription(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    db_subscription = Subscriptions(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


@app.post('/subscriptions/services/', response_model=ServiceResponse)
async def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    db_service = Services(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service
