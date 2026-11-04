from typing import List, Optional
from uuid import UUID
from datetime import date
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.models.models import User, DealStatus
from src.schemas.deal import DealCreate, DealUpdate, DealResponse
from src.crud import deal as crud_deal
from src.core.auth import get_current_user

router = APIRouter(prefix="/deals", tags=["Deals"])

@router.post("/", response_model=DealResponse, status_code=status.HTTP_201_CREATED)
def create_deal(
    deal_in: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return crud_deal.create_deal(db=db, deal_in=deal_in, current_user=current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[DealResponse])
def read_deals(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    deal_status: Optional[DealStatus] = Query(None, alias="status"),
    customer_id: Optional[UUID] = None,
    owner_id: Optional[UUID] = None,
    min_amount: Optional[Decimal] = Query(None, ge=Decimal("0")),
    max_amount: Optional[Decimal] = Query(None, ge=Decimal("0")),
    min_probability: Optional[int] = Query(None, ge=0, le=100),
    max_probability: Optional[int] = Query(None, ge=0, le=100),
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_deal.get_deals(
        db=db, 
        current_user=current_user, 
        skip=skip, 
        limit=limit, 
        deal_status=deal_status, 
        customer_id=customer_id,
        owner_id=owner_id,
        min_amount=min_amount,
        max_amount=max_amount,
        min_probability=min_probability,
        max_probability=max_probability,
        date_from=date_from,
        date_to=date_to
    )

@router.get("/{deal_id}", response_model=DealResponse)
def read_deal(
    deal_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deal = crud_deal.get_deal(db=db, deal_id=deal_id, current_user=current_user)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal

@router.patch("/{deal_id}", response_model=DealResponse)
def update_deal(
    deal_id: UUID,
    deal_in: DealUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deal = crud_deal.get_deal(db=db, deal_id=deal_id, current_user=current_user)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    try:
        return crud_deal.update_deal(db=db, db_deal=deal, deal_in=deal_in, current_user=current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{deal_id}", response_model=DealResponse)
def delete_deal(
    deal_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deal = crud_deal.get_deal(db=db, deal_id=deal_id, current_user=current_user)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return crud_deal.delete_deal(db=db, db_deal=deal)