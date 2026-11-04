from datetime import datetime, timezone, date
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.models.models import Deal, DealStatus, User, Customer
from src.schemas.deal import DealCreate, DealUpdate

STAGE_ORDER = {
    DealStatus.new: 1,
    DealStatus.qualified: 2,
    DealStatus.proposal: 3,
    DealStatus.negotiation: 4,
    DealStatus.won: 5,
    DealStatus.lost: 5,
}

def get_deal(db: Session, deal_id: UUID, current_user: User) -> Optional[Deal]:
    query = select(Deal).where(Deal.id == deal_id, Deal.deleted_at.is_(None))
    if current_user.role != "Admin":
        query = query.where(Deal.owner_id == current_user.id)
    return db.execute(query).scalar_one_or_none()

def get_deals(
    db: Session, 
    current_user: User, 
    skip: int = 0, 
    limit: int = 20,
    deal_status: Optional[DealStatus] = None,
    customer_id: Optional[UUID] = None,
    owner_id: Optional[UUID] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    min_probability: Optional[int] = None,
    max_probability: Optional[int] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None
) -> List[Deal]:
    query = select(Deal).where(Deal.deleted_at.is_(None))
    
    if current_user.role != "Admin":
        query = query.where(Deal.owner_id == current_user.id)
    elif owner_id:
        query = query.where(Deal.owner_id == owner_id)
        
    if deal_status:
        query = query.where(Deal.status == deal_status)
    if customer_id:
        query = query.where(Deal.customer_id == customer_id)
    if min_amount is not None:
        query = query.where(Deal.amount >= min_amount)
    if max_amount is not None:
        query = query.where(Deal.amount <= max_amount)
    if min_probability is not None:
        query = query.where(Deal.probability >= min_probability)
    if max_probability is not None:
        query = query.where(Deal.probability <= max_probability)
    if date_from is not None:
        query = query.where(Deal.expected_close_date >= date_from)
    if date_to is not None:
        query = query.where(Deal.expected_close_date <= date_to)
        
    query = query.order_by(Deal.created_at.desc(), Deal.id).offset(skip).limit(limit)
    return db.execute(query).scalars().all()

def create_deal(db: Session, deal_in: DealCreate, current_user: User) -> Deal:
    customer_query = select(Customer).where(Customer.id == deal_in.customer_id, Customer.deleted_at.is_(None))
    if current_user.role != "Admin":
        customer_query = customer_query.where(Customer.owner_id == current_user.id)
    customer = db.execute(customer_query).scalar_one_or_none()
    
    if not customer:
        raise ValueError("Customer not found or access denied")

    db_deal = Deal(
        title=deal_in.title,
        amount=deal_in.amount,
        probability=deal_in.probability,
        expected_close_date=deal_in.expected_close_date,
        status=deal_in.status or DealStatus.new,
        customer_id=deal_in.customer_id,
        owner_id=current_user.id
    )
    
    if db_deal.status in [DealStatus.won, DealStatus.lost]:
        db_deal.closed_at = datetime.now(timezone.utc)
        
    try:
        db.add(db_deal)
        db.commit()
        db.refresh(db_deal)
        return db_deal
    except SQLAlchemyError:
        db.rollback()
        raise

def update_deal(db: Session, db_deal: Deal, deal_in: DealUpdate, current_user: User) -> Deal:
    update_data = deal_in.model_dump(exclude_unset=True)
    
    if "owner_id" in update_data:
        if current_user.role != "Admin":
            raise ValueError("Only Admin can reassign deal owner")
    
    if "status" in update_data and update_data["status"] != db_deal.status:
        if db_deal.status in [DealStatus.won, DealStatus.lost]:
            raise ValueError("Cannot change status of a closed deal")
            
        new_status = update_data["status"]
        current_rank = STAGE_ORDER.get(db_deal.status, 0)
        new_rank = STAGE_ORDER.get(new_status, 0)
        
        if new_rank < current_rank:
            raise ValueError(f"Cannot move deal status backward from {db_deal.status} to {new_status}")
            
        if new_status in [DealStatus.won, DealStatus.lost]:
            db_deal.closed_at = datetime.now(timezone.utc)
        else:
            db_deal.closed_at = None

    for field, value in update_data.items():
        setattr(db_deal, field, value)
        
    try:
        db.commit()
        db.refresh(db_deal)
        return db_deal
    except SQLAlchemyError:
        db.rollback()
        raise

def delete_deal(db: Session, db_deal: Deal) -> Deal:
    db_deal.deleted_at = datetime.now(timezone.utc)
    try:
        db.commit()
        db.refresh(db_deal)
        return db_deal
    except SQLAlchemyError:
        db.rollback()
        raise