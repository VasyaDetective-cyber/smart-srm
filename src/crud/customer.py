from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone

from src.models.models import Customer
from src.schemas.customer import CustomerCreate, CustomerUpdate

def get_customer(db: Session, customer_id: UUID, user_id: UUID, is_admin: bool = False):
    query = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.deleted_at.is_(None),
    )
    if not is_admin:
        query = query.filter(Customer.owner_id == user_id)
    return query.first()

def get_customers(db: Session, user_id: UUID, is_admin: bool = False, skip: int = 0, limit: int = 100):
    query = db.query(Customer).filter(Customer.deleted_at.is_(None))
    if not is_admin:
        query = query.filter(Customer.owner_id == user_id)
    return query.offset(skip).limit(limit).all()

def create_customer(db: Session, customer: CustomerCreate, owner_id: UUID):
    db_customer = Customer(**customer.model_dump(), owner_id=owner_id)
    try:
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except Exception:
        db.rollback()
        raise

def update_customer(db: Session, customer_id: UUID, customer_update: CustomerUpdate, user_id: UUID, is_admin: bool = False):
    db_customer = get_customer(db, customer_id, user_id, is_admin)
    if not db_customer:
        return None
    
    update_data = customer_update.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)
        
    try:
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except Exception:
        db.rollback()
        raise

def delete_customer(db: Session, customer_id: UUID, user_id: UUID, is_admin: bool = False):
    db_customer = get_customer(db, customer_id, user_id, is_admin)
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