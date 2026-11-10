from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.models.models import User


def get_user(db: Session, user_id: UUID) -> Optional[User]:
    query = select(User).where(
        User.id == user_id,
        User.deleted_at.is_(None)
    )

    return db.execute(query).scalar_one_or_none()


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 20
) -> List[User]:

    query = (
        select(User)
        .where(User.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )

    return db.execute(query).scalars().all()


def update_user(
    db: Session,
    db_user: User,
    user_in: dict
) -> User:

    for field, value in user_in.items():
        setattr(db_user, field, value)

    try:
        db.commit()
        db.refresh(db_user)
        return db_user

    except IntegrityError:
        db.rollback()
        raise

    except SQLAlchemyError:
        db.rollback()
        raise


def delete_user(db: Session, db_user: User) -> User:
    db_user.deleted_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(db_user)
        return db_user

    except SQLAlchemyError:
        db.rollback()
        raise