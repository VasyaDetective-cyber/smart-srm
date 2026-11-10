from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.models.models import User
from src.schemas.user import UserRead, UserCreate
from src.crud import user as crud_user
from src.core.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserRead])
def read_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return crud_user.get_users(db=db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserRead)
def read_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "Admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    db_user = crud_user.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: UUID,
    user_in: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "Admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    db_user = crud_user.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if "role" in user_in and current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin can change user roles"
        )
        
    return crud_user.update_user(db=db, db_user=db_user, user_in=user_in)

@router.delete("/{user_id}", response_model=UserRead)
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin can delete users"
        )
    db_user = crud_user.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.delete_user(db=db, db_user=db_user)