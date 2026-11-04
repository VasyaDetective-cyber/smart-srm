from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class ContactBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    title: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^\+?[0-9\s\-\(\)]{5,20}$")

class ContactCreate(ContactBase):
    customer_id: UUID

class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    title: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^\+?[0-9\s\-\(\)]{5,20}$")

class ContactResponse(ContactBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: UUID
    created_at: datetime
    updated_at: datetime