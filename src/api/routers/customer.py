from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.db.database import get_db
from src.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from src.crud import customer as crud_customer

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return crud_customer.create_customer(db=db, customer=customer)

@router.get("/", response_model=List[CustomerResponse])
def read_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    return crud_customer.get_customers(db=db, skip=skip, limit=limit)

@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: UUID, db: Session = Depends(get_db)):
    db_customer = crud_customer.get_customer(db=db, customer_id=customer_id)
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return db_customer

@router.patch("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: UUID, customer_update: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = crud_customer.update_customer(db=db, customer_id=customer_id, customer_update=customer_update)
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return db_customer

@router.delete("/{customer_id}", response_model=CustomerResponse)
def delete_customer(customer_id: UUID, db: Session = Depends(get_db)):
    db_customer = crud_customer.delete_customer(db=db, customer_id=customer_id)
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return db_customer