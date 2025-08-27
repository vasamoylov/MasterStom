from fastapi import HTTPException, Depends
from app.models.schemas import (ClientCreate, SubscriptionCreate, CategoryCreate, ServiceCreate,
                                SubscriptionServicesCreate, ClientSubscriptionCreate, OfferCreate, ContactCreate,
                                ClientResponse, SubscriptionResponse, CategoryResponse, ServiceResponse,
                                SubscriptionServicesResponse, OfferResponse, ContactResponse)
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models.db_models import (Clients, Subscriptions, Services, ClientSubscriptions, ServicesAvailability,
                                  Categories, SubscriptionServices, Offers, Contacts)

from fastapi import FastAPI

app = FastAPI(
    title='MasterStom Clients',
    description='Clients and Subscriptoins'
)


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


@app.get('/clients/{id}/', response_model=ClientResponse)
async def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.get(Clients, client_id)
    if not client:
        raise HTTPException(status_code=404, detail='Client not found')
    return client


@app.put('/clients/{id}/', response_model=ClientResponse)
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


@app.delete('/clients/{id}/')
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.get(Clients, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail='Client not found')
    db.delete(db_client)
    db.commit()
    return {'message': 'Client deleted'}


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


@app.put('/subscriptions/{id}/', response_model=SubscriptionResponse)
async def get_subscription(subscription_id, subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    db_subscription = db.get(Subscriptions, subscription_id)
    if not db_subscription:
        raise HTTPException(status_code=404, detail='Subscription not found')
    db_subscription.name = subscription.name
    db_subscription.price = subscription.price
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


@app.delete('/subscriptions/{id}/')
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


@app.put('/categories/{id}/', response_model=CategoryResponse)
async def update_category(category_id, category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.get(Categories, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail='Category not found')
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category


@app.delete('/categories/{id}/')
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.get(Categories, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail='Category not found')
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


@app.put('/services/{id}/', response_model=ServiceResponse)
async def update_service(service_id, service: ServiceCreate, db: Session = Depends(get_db)):
    db_service = db.get(Services, service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail='Service not found')
    db_service.category_id = service.category_id
    db_service.description = service.description
    db_service.price = service.price
    db.commit()
    db.refresh(db_service)
    return db_service


@app.delete('/services/{id}/')
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    db_service = db.get(Services, service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail='Service not found')
    db.delete(db_service)
    db.commit()
    return {'message': 'Service deleted'}


@app.post('/subscription/services/', response_model=SubscriptionServicesResponse)
async def create_subscription_service(subscription_service: SubscriptionServicesCreate, db: Session = Depends(get_db)):
    db_subscription_service = SubscriptionServices(**subscription_service.dict())
    db.add(db_subscription_service)
    db.commit()
    db.refresh(db_subscription_service)
    return db_subscription_service


@app.get('/subscription/services/')
async def get_subscription_services(db: Session = Depends(get_db)):
    subscription_services = db.query(SubscriptionServices).all()
    return subscription_services


@app.put('/subscription/services/{id}/', response_model=SubscriptionServicesResponse)
async def update_subscription_service(
        subscription_service_id, subscription_service: SubscriptionServicesCreate, db: Session = Depends(get_db)):
    db_subscription_service = db.get(SubscriptionServices, subscription_service_id)
    if not db_subscription_service:
        raise HTTPException(status_code=404, detail='Service not found')
    db_subscription_service.service_id = subscription_service.service_id
    db_subscription_service.subscription_id = subscription_service.subscription_id
    db_subscription_service.quantity = subscription_service.quantity
    db.commit()
    db.refresh(db_subscription_service)
    return db_subscription_service


@app.delete('/subscription/services/{id}/')
async def delete_subscription_service(subscription_service_id: int, db: Session = Depends(get_db)):
    db_subscription_service = db.get(SubscriptionServices, subscription_service_id)
    if not db_subscription_service:
        raise HTTPException(status_code=404, detail='Service not found')
    db.delete(db_subscription_service)
    db.commit()
    return {'message': 'Service deleted'}


@app.post('/clients/subscription/')
async def create_client_subscription(client_subscription: ClientSubscriptionCreate, db: Session = Depends(get_db)):
    db_client_subscription = ClientSubscriptions(**client_subscription.dict())
    db.add(db_client_subscription)
    service_availability = (
        db.query(
            SubscriptionServices.service_id, SubscriptionServices.quantity).filter_by(
            subscription_id=db_client_subscription.subscription_id).all()
    )
    for service in service_availability:
        db_service = ServicesAvailability(
            client_id=db_client_subscription.client_id,
            service_id=service.service_id,
            quantity=service.quantity)
        db.add(db_service)
    db.commit()
    db.refresh(db_client_subscription)
    return {'message': 'Subscription completed successfully'}


@app.get('/clients/subscription/')
async def get_clients_subscriptions(db: Session = Depends(get_db)):
    clients_subscriptions = db.query(ClientSubscriptions).all()
    return clients_subscriptions


@app.get('/clients/{id}/subscription/')
async def get_client_subscription(client_id: int, db: Session = Depends(get_db)):
    client = db.get(ClientSubscriptions, client_id)
    if not client:
        raise HTTPException(status_code=404, detail='Client not have subscription')
    else:
        client_subscription = db.query(ClientSubscriptions).filter_by(client_id=client_id).one()
    return client_subscription


@app.put('/clients/{id}/subscription/')
async def update_client_subscription(
        client_id: int,
        client_subscription: ClientSubscriptionCreate,
        db: Session = Depends(get_db)
):
    # Проверка клиента
    db_client = db.query(ClientSubscriptions).filter_by(client_id=client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail='Client not found')

    # Проверка подписки
    subscription_exists = db.query(ClientSubscriptions).filter_by(client_id=client_id).first()
    if not subscription_exists:
        raise HTTPException(status_code=404, detail='Subscription not found')

    # Обновляем ID подписки
    db_client.subscription_id = client_subscription.subscription_id

    # Получаем текущие услуги клиента
    current_services = db.query(
        ServicesAvailability.service_id,
        ServicesAvailability.quantity
    ).filter_by(client_id=client_id).all()

    # Получаем услуги новой подписки
    new_services = db.query(
        SubscriptionServices.service_id,
        SubscriptionServices.quantity
    ).filter_by(subscription_id=db_client.subscription_id).all()

    # Создаем словари для объединения
    current_dict = {row.service_id: row.quantity for row in current_services}
    new_dict = {row.service_id: row.quantity for row in new_services}

    # Суммируем услуги
    for service_id, quantity in new_dict.items():
        if service_id in current_dict:
            current_dict[service_id] += quantity
        else:
            current_dict[service_id] = quantity

        # Обновляем существующие записи
    for service_id, quantity in current_dict.items():
        # Проверяем, была ли услуга у клиента ранее
        existing_service = db.query(ServicesAvailability).filter_by(
            client_id=client_id, service_id=service_id
        ).first()

        if existing_service:
            # Обновляем существующую запись
            existing_service.quantity = quantity
        else:
            # Добавляем новую услугу
            db.add(ServicesAvailability(client_id=client_id, service_id=service_id, quantity=quantity))

        db.commit()

    db.refresh(db_client)
    return {'message': 'Client subscription updated'}


@app.delete('/clients/subscription/{id}/')
async def delete_client_subscription(client_subscription_id: int, db: Session = Depends(get_db)):
    db_client_subscription = db.get(ClientSubscriptions, client_subscription_id)
    if not db_client_subscription:
        raise HTTPException(status_code=404, detail='Client subscription not found')
    db_client_id = db_client_subscription.client_id
    db.query(ServicesAvailability).filter_by(client_id=db_client_id).delete()
    db.delete(db_client_subscription)
    db.commit()
    return {'message': 'Client subscription deleted'}


@app.put('/clients/{id}/subscription/services/')
async def use_availability_services(client_id: int, service_id: int, quantity: int, db: Session = Depends(get_db)):
    db_availability = (
        db.query(ServicesAvailability).filter_by(client_id=client_id, service_id=service_id)).first()
    if not db_availability:
        raise HTTPException(status_code=404, detail='This service is not included in the subscription')
    if db_availability.quantity < quantity:
        raise HTTPException(status_code=400, detail='Not enough available services')
    db_availability.quantity -= quantity
    db.commit()
    return {'message': 'The service was successfully used'}


@app.post('/offers/', response_model=OfferResponse)
async def create_offer(offer: OfferCreate, db: Session = Depends(get_db)):
    db_offer = Offers(**offer.dict())
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer


@app.get('/offers/')
async def get_offers(db: Session = Depends(get_db)):
    offers = db.query(Offers).all()
    return offers


@app.put('/offers/{id}/', response_model=OfferResponse)
async def update_offer(offer_id, offer: OfferCreate, db: Session = Depends(get_db)):
    db_offer = db.get(Offers, offer_id)
    if not db_offer:
        raise HTTPException(status_code=404, detail='Offer not found')
    db_offer.name = offer.name
    db_offer.url = offer.url
    db.commit()
    db.refresh(db_offer)
    return db_offer


@app.delete('/offers/{id}/')
async def delete_category(offer_id: int, db: Session = Depends(get_db)):
    db_offer = db.get(Offers, offer_id)
    if not db_offer:
        raise HTTPException(status_code=404, detail='Offer not found')
    db.delete(db_offer)
    db.commit()
    return {'message': 'Offer deleted'}


@app.post('/contacts/', response_model=ContactResponse)
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contacts(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.get('/contacts/')
async def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contacts).all()
    return contacts


@app.delete('/contacts/{id}/')
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.get(Contacts, contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail='Contact not found')
    db.delete(db_contact)
    db.commit()
    return {'message': 'Contact deleted'}
