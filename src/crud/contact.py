from typing import Optional
from uuid import UUID
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.models import Contact, Customer
from src.schemas.contact import ContactCreate, ContactUpdate

def get_contact(db: Session, contact_id: UUID, user_id: UUID, is_admin: bool = False):
    query = db.query(Contact).join(Customer, Contact.customer_id == Customer.id).filter(
        Contact.id == contact_id,
        Contact.deleted_at.is_(None),
        Customer.deleted_at.is_(None),
    )
    if not is_admin:
        query = query.filter(Customer.owner_id == user_id)
    return query.first()

def get_contacts(db: Session, user_id: UUID, is_admin: bool = False, customer_id: Optional[UUID] = None, skip: int = 0, limit: int = 100):
    query = db.query(Contact).join(Customer, Contact.customer_id == Customer.id).filter(
        Contact.deleted_at.is_(None),
        Customer.deleted_at.is_(None),
    )
    if not is_admin:
        query = query.filter(Customer.owner_id == user_id)
    if customer_id:
        query = query.filter(Contact.customer_id == customer_id)
    return query.offset(skip).limit(limit).all()

def create_contact(db: Session, contact: ContactCreate, user_id: UUID, is_admin: bool = False):
    customer_query = db.query(Customer).filter(
        Customer.id == contact.customer_id,
        Customer.deleted_at.is_(None),
    )
    if not is_admin:
        customer_query = customer_query.filter(Customer.owner_id == user_id)
    customer = customer_query.first()
    if not customer:
        return None

    if contact.email:
        existing_email = db.query(Contact).filter(
            Contact.customer_id == contact.customer_id,
            Contact.email == contact.email,
            Contact.deleted_at.is_(None),
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Contact with this email already exists for this customer"
            )

    db_contact = Contact(**contact.model_dump())
    try:
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Contact with this email already exists for this customer"
        )
    except Exception:
        db.rollback()
        raise

def update_contact(db: Session, contact_id: UUID, contact_update: ContactUpdate, user_id: UUID, is_admin: bool = False):
    db_contact = get_contact(db, contact_id, user_id, is_admin)
    if not db_contact:
        return None

    update_data = contact_update.model_dump(exclude_unset=True)

    for non_nullable in ["first_name", "last_name"]:
        if non_nullable in update_data and update_data[non_nullable] is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Field '{non_nullable}' cannot be null"
            )

    if update_data.get("email"):
        existing_email = db.query(Contact).filter(
            Contact.customer_id == db_contact.customer_id,
            Contact.email == update_data["email"],
            Contact.id != contact_id,
            Contact.deleted_at.is_(None),
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Contact with this email already exists for this customer"
            )

    for key, value in update_data.items():
        setattr(db_contact, key, value)

    try:
        db.commit()
        db.refresh(db_contact)
        return db_contact
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Contact with this email already exists for this customer"
        )
    except Exception:
        db.rollback()
        raise

def delete_contact(db: Session, contact_id: UUID, user_id: UUID, is_admin: bool = False):
    db_contact = get_contact(db, contact_id, user_id, is_admin)
    if not db_contact:
        return None

    db_contact.deleted_at = datetime.now(timezone.utc)
    try:
        db.commit()
        db.refresh(db_contact)
        return db_contact
    except Exception:
        db.rollback()
        raise