from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from src.models.models import DealStatus


class DealInputBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    amount: Decimal = Field(..., gt=0, le=Decimal("9999999999999.99"))
    probability: int = Field(..., ge=0, le=100)
    expected_close_date: date

    @field_validator("title", mode="before")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        if not isinstance(value, str):
            return value
        value = value.strip()
        if not value:
            raise ValueError("Deal title cannot be empty")
        return value

    @field_validator("expected_close_date")
    @classmethod
    def validate_close_date(cls, value: date) -> date:
        if value <= date.today():
            raise ValueError("Expected close date must be in the future")
        return value


class DealCreate(DealInputBase):
    customer_id: UUID


class DealUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[Decimal] = Field(None, gt=0, le=Decimal("9999999999999.99"))
    probability: Optional[int] = Field(None, ge=0, le=100)
    expected_close_date: Optional[date] = None
    status: Optional[DealStatus] = None
    customer_id: Optional[UUID] = None
    owner_id: Optional[UUID] = None

    @model_validator(mode="before")
    @classmethod
    def reject_explicit_nulls(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for field in data:
                if data[field] is None:
                    raise ValueError(f"{field} cannot be null")
        return data

    @field_validator("title", mode="before")
    @classmethod
    def normalize_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("Deal title cannot be empty")
        return value

    @field_validator("expected_close_date")
    @classmethod
    def validate_close_date(cls, value: Optional[date]) -> Optional[date]:
        if value is not None and value <= date.today():
            raise ValueError("Expected close date must be in the future")
        return value


class DealResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    amount: Decimal
    probability: int
    expected_close_date: date
    id: UUID
    customer_id: UUID
    owner_id: UUID
    status: DealStatus
    closed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
