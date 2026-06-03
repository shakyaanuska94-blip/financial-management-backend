from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.database import get_db
from app.models.models import Client, ClientPayment
from app.schemas.schemas import ClientCreate, ClientOut, ClientPaymentCreate, ClientPaymentOut

router = APIRouter()

@router.post("/clients", response_model=ClientOut, tags=["Clients"])
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client = Client(**client.model_dump())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@router.get("/clients", response_model=List[ClientOut], tags=["Clients"])
def get_all_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@router.get("/clients/{client_id}", response_model=ClientOut, tags=["Clients"])
def get_client(client_id: UUID, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/clients/{client_id}", response_model=ClientOut, tags=["Clients"])
def update_client(client_id: UUID, updated: ClientCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in updated.model_dump().items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client

@router.delete("/clients/{client_id}", tags=["Clients"])
def delete_client(client_id: UUID, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return {"message": "Client deleted successfully"}

@router.post("/client-payments", response_model=ClientPaymentOut, tags=["Client Payments"])
def create_client_payment(payment: ClientPaymentCreate, db: Session = Depends(get_db)):
    new_payment = ClientPayment(**payment.model_dump())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("/client-payments", response_model=List[ClientPaymentOut], tags=["Client Payments"])
def get_client_payments(db: Session = Depends(get_db)):
    return db.query(ClientPayment).all()