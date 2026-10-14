from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone

from src.models.models import Customer
from src.schemas.customer import CustomerCreate, CustomerUpdate

def get_customer(db: Session, customer_id: UUID):
    return (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.deleted_at.is_(None),
        )
        .first()
    )

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Customer)
        .filter(Customer.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_customer(db: Session, customer: CustomerCreate):
    db_customer = Customer(**customer.model_dump())
    try:
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except Exception:
        db.rollback()
        raise

def update_customer(db: Session, customer_id: UUID, customer_update: CustomerUpdate):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
    
    update_data = customer_update.model_dump(exclude_unset=True, exclude={"owner_id"})
    for key, value in update_data.items():
        setattr(db_customer, key, value)
        
    try:
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except Exception:
        db.rollback()
        raise

def delete_customer(db: Session, customer_id: UUID):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
        
    db_customer.deleted_at = datetime.now(timezone.utc)
    try:
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except Exception:
        db.rollback()
        raise