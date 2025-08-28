from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import date


class ClientCreate(BaseModel):
    name: str
    surname: str
    patronymic: str
    age: int
    phone: PhoneNumber
    email: EmailStr
    password: str


class SubscriptionCreate(BaseModel):
    name: str
    price: int


class CategoryCreate(BaseModel):
    name: str


class ServiceCreate(BaseModel):
    category_id: int
    description: str
    price: int


class SubscriptionServicesCreate(BaseModel):
    service_id: int
    subscription_id: int
    quantity: int


class ClientSubscriptionCreate(BaseModel):
    client_id: int
    subscription_id: int
    start_date: date
    end_date: date


class OfferCreate(BaseModel):
    name: str
    url: str


class ContactCreate(BaseModel):
    name: str
    url: str


class ClientResponse(ClientCreate):
    id: int


class SubscriptionResponse(SubscriptionCreate):
    id: int


class CategoryResponse(CategoryCreate):
    id: int


class ServiceResponse(ServiceCreate):
    id: int


class SubscriptionServicesResponse(SubscriptionServicesCreate):
    id: int


class OfferResponse(OfferCreate):
    id: int


class ContactResponse(ContactCreate):
    id: int
