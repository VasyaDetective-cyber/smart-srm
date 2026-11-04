from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from src.crud import contact as crud_contact
from src.models.models import User
from src.core.auth import get_current_user

router = APIRouter(prefix="/contacts", tags=["Contacts"])

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    is_admin = current_user.role == 'Admin'
    db_contact = crud_contact.create_contact(
        db=db,
        contact=contact,
        user_id=current_user.id,
        is_admin=is_admin
    )
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return db_contact

@router.get("/", response_model=List[ContactResponse])
def read_contacts(
    customer_id: Optional[UUID] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    is_admin = current_user.role == 'Admin'
    return crud_contact.get_contacts(
        db=db,
        user_id=current_user.id,
        is_admin=is_admin,
        customer_id=customer_id,
        skip=skip,
        limit=limit
    )

@router.get("/{contact_id}", response_model=ContactResponse)
def read_contact(
    contact_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    is_admin = current_user.role == 'Admin'
    db_contact = crud_contact.get_contact(
        db=db,
        contact_id=contact_id,
        user_id=current_user.id,
        is_admin=is_admin
    )
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    return db_contact

@router.patch("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: UUID,
    contact_update: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not contact_update.model_dump(exclude_unset=True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )

    is_admin = current_user.role == 'Admin'
    db_contact = crud_contact.update_contact(
        db=db,
        contact_id=contact_id,
        contact_update=contact_update,
        user_id=current_user.id,
        is_admin=is_admin
    )
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    return db_contact

@router.delete("/{contact_id}", response_model=ContactResponse)
def delete_contact(
    contact_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    is_admin = current_user.role == 'Admin'
    db_contact = crud_contact.delete_contact(
        db=db,
        contact_id=contact_id,
        user_id=current_user.id,
        is_admin=is_admin
    )
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    return db_contact