from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    segment_id: Optional[str] = None
    churn_score: Optional[float] = 0.0
    custom_fields: Optional[Dict[str, Any]] = {}


class CustomerCreate(CustomerBase):
    id: str
    organization_id: int


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    segment_id: Optional[str] = None
    churn_score: Optional[float] = None
    custom_fields: Optional[Dict[str, Any]] = None


class CustomerResponse(CustomerBase):
    id: str
    organization_id: int

    class Config:
        from_attributes = True


class SegmentResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    customer_count: Optional[int] = 0
