from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    industry: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, min_length=5, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    industry: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, min_length=5, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = None

class CustomerResponse(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime