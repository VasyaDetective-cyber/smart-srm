from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.models.models import Customer, Deal, DealStatus, User
from src.schemas.deal import DealCreate, DealUpdate


ALLOWED_STATUS_TRANSITIONS = {
    DealStatus.new: {DealStatus.qualified},
    DealStatus.qualified: {DealStatus.proposal},
    DealStatus.proposal: {DealStatus.negotiation},
    DealStatus.negotiation: {DealStatus.won, DealStatus.lost},
    DealStatus.won: set(),
    DealStatus.lost: set(),
}


def _visible_customer_query(db: Session, current_user: User):
    query = select(Customer).where(Customer.deleted_at.is_(None))
    if current_user.role != "Admin":
        query = query.where(Customer.owner_id == current_user.id)
    return query


def get_deal(db: Session, deal_id: UUID, current_user: User) -> Optional[Deal]:
    query = (
        select(Deal)
        .join(Customer, Deal.customer_id == Customer.id)
        .where(Deal.id == deal_id, Deal.deleted_at.is_(None), Customer.deleted_at.is_(None))
    )
    if current_user.role != "Admin":
        query = query.where(Deal.owner_id == current_user.id)
    return db.execute(query).scalar_one_or_none()


def get_deals(
    db: Session,
    current_user: User,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    deal_status: Optional[DealStatus] = None,
    customer_id: Optional[UUID] = None,
    owner_id: Optional[UUID] = None,
    min_amount: Optional[Decimal] = None,
    max_amount: Optional[Decimal] = None,
    min_probability: Optional[int] = None,
    max_probability: Optional[int] = None,
    date_from=None,
    date_to=None,
) -> List[Deal]:
    query = (
        select(Deal)
        .join(Customer, Deal.customer_id == Customer.id)
        .where(Deal.deleted_at.is_(None), Customer.deleted_at.is_(None))
    )

    if current_user.role != "Admin":
        query = query.where(Deal.owner_id == current_user.id)
    elif owner_id:
        query = query.where(Deal.owner_id == owner_id)

    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.where(or_(Deal.title.ilike(term), Customer.name.ilike(term)))
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
    customer = db.execute(_visible_customer_query(db, current_user).where(Customer.id == deal_in.customer_id)).scalar_one_or_none()
    if not customer:
        raise ValueError("Customer not found or access denied")

    db_deal = Deal(
        title=deal_in.title,
        amount=deal_in.amount,
        probability=deal_in.probability,
        expected_close_date=deal_in.expected_close_date,
        status=DealStatus.new,
        customer_id=deal_in.customer_id,
        owner_id=current_user.id,
    )
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
    if not update_data:
        raise ValueError("No fields provided for update")

    if "owner_id" in update_data:
        if current_user.role != "Admin":
            raise ValueError("Only Admin can reassign deal owner")
        owner = db.execute(select(User).where(User.id == update_data["owner_id"], User.deleted_at.is_(None))).scalar_one_or_none()
        if not owner:
            raise ValueError("Owner not found")

    if "customer_id" in update_data:
        customer = db.execute(_visible_customer_query(db, current_user).where(Customer.id == update_data["customer_id"])).scalar_one_or_none()
        if not customer:
            raise ValueError("Customer not found or access denied")

    if "status" in update_data and update_data["status"] != db_deal.status:
        allowed = ALLOWED_STATUS_TRANSITIONS.get(db_deal.status, set())
        if update_data["status"] not in allowed:
            raise ValueError(f"Invalid status transition from {db_deal.status} to {update_data['status']}")
        if update_data["status"] in {DealStatus.won, DealStatus.lost}:
            db_deal.closed_at = datetime.now(timezone.utc)

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
