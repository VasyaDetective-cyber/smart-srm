import uuid
from sqlalchemy import Column, String, Integer, Text, ForeignKey, Numeric, Date, DateTime, Enum, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum('Manager', 'Admin', name='user_role'), nullable=False, default='Manager')
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    customers = relationship("Customer", back_populates="owner")
    deals = relationship("Deal", back_populates="owner")
    activities = relationship("Activity", back_populates="creator")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    industry = Column(String(100))
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    address = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    owner = relationship("User", back_populates="customers")
    contacts = relationship("Contact", back_populates="customer")
    deals = relationship("Deal", back_populates="customer")
    activities = relationship("Activity", back_populates="customer")


class Contact(Base):
    __tablename__ = "contacts"
    __table_args__ = (
        UniqueConstraint('customer_id', 'email', name='uq_contact_customer_email'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="RESTRICT"), nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    title = Column(String(100))
    email = Column(String(255))
    phone = Column(String(20))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    customer = relationship("Customer", back_populates="contacts")


class Deal(Base):
    __tablename__ = "deals"
    __table_args__ = (
        CheckConstraint('probability >= 0 AND probability <= 100', name='check_probability_range'),
        CheckConstraint('amount > 0 AND amount <= 999999999.99', name='check_amount_range'),
        CheckConstraint(
            "(status IN ('Won', 'Lost')) = (closed_at IS NOT NULL)",
            name="check_closed_at_matches_status"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="RESTRICT"), nullable=False, index=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    amount = Column(Numeric(11, 2), nullable=False)
    probability = Column(Integer, nullable=False)
    status = Column(Enum('New', 'Qualified', 'Proposal', 'Negotiation', 'Won', 'Lost', name='deal_status'), nullable=False, default='New', index=True)
    expected_close_date = Column(Date, nullable=False)
    closed_at = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    customer = relationship("Customer", back_populates="deals")
    owner = relationship("User", back_populates="deals")
    activities = relationship("Activity", back_populates="deal")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="RESTRICT"), nullable=False, index=True)
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id", ondelete="RESTRICT"), index=True)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    activity_type = Column(Enum('Call', 'Meeting', 'Email', 'Note', name='activity_type_enum'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    scheduled_date = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    customer = relationship("Customer", back_populates="activities")
    deal = relationship("Deal", back_populates="activities")
    creator = relationship("User", back_populates="activities")