from datetime import date, datetime
from typing import Optional, Any
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, model_validator
from src.models.models import DealStatus

class DealBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    amount: Decimal = Field(..., gt=0, le=Decimal("999999999.99"))
    probability: int = Field(..., ge=0, le=100)
    expected_close_date: date

    @field_validator('expected_close_date')
    @classmethod
    def validate_close_date(cls, v: date) -> date:
        if v < date.today():
            raise ValueError('Expected close date cannot be in the past')
        return v

class DealCreate(DealBase):
    customer_id: UUID
    owner_id: Optional[UUID] = None

class DealUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[Decimal] = Field(None, gt=0, le=Decimal("999999999.99"))
    probability: Optional[int] = Field(None, ge=0, le=100)
    expected_close_date: Optional[date] = None
    status: Optional[DealStatus] = None
    customer_id: Optional[UUID] = None
    owner_id: Optional[UUID] = None

    @model_validator(mode='before')
    @classmethod
    def check_no_nulls(cls, data: Any) -> Any:
        if isinstance(data, dict):
            required_fields = ['title', 'amount', 'probability', 'expected_close_date', 'status', 'customer_id', 'owner_id']
            for field in required_fields:
                if field in data and data[field] is None:
                    raise ValueError(f"{field} cannot be null")
        return data

    @field_validator('expected_close_date')
    @classmethod
    def validate_close_date(cls, v: Optional[date]) -> Optional[date]:
        if v and v < date.today():
            raise ValueError('Expected close date cannot be in the past')
        return v

class DealResponse(DealBase):
    id: UUID
    customer_id: UUID
    owner_id: UUID
    status: DealStatus
    closed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True