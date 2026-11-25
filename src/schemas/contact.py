from datetime import datetime
from typing import Optional
from uuid import UUID

import re
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


PHONE_RE = re.compile(r"[+0-9()\-\s]{5,20}")


class ContactBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    title: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=5, max_length=20)

    @field_validator("first_name", "last_name", "title", mode="before")
    @classmethod
    def normalize_text(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        return value or None

    @field_validator("first_name", "last_name")
    @classmethod
    def require_name(cls, value: str) -> str:
        if not value:
            raise ValueError("Contact name cannot be empty")
        return value

    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value = value.strip()
        if not value:
            return None
        if not PHONE_RE.fullmatch(value):
            raise ValueError("Invalid phone format")
        return value


class ContactCreate(ContactBase):
    customer_id: UUID


class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    title: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=5, max_length=20)

    @field_validator("first_name", "last_name", mode="before")
    @classmethod
    def require_update_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            raise ValueError("Contact name cannot be null")
        value = value.strip()
        if not value:
            raise ValueError("Contact name cannot be empty")
        return value

    @field_validator("title", mode="before")
    @classmethod
    def normalize_update_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value = value.strip()
        return value or None

    @field_validator("phone", mode="before")
    @classmethod
    def validate_update_phone(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value = value.strip()
        if not value:
            return None
        if not PHONE_RE.fullmatch(value):
            raise ValueError("Invalid phone format")
        return value


class ContactResponse(ContactBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: UUID
    created_at: datetime
    updated_at: datetime
