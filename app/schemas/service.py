from decimal import Decimal

from pydantic import BaseModel, Field


class ServiceCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: str | None = None
    price: Decimal = Field(..., gt=0)
    is_active: bool = True


class ServiceUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=150)
    description: str | None = None
    price: Decimal | None = Field(None, gt=0)
    is_active: bool | None = None


class ServiceResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    is_active: bool

    class Config:
        from_attributes = True