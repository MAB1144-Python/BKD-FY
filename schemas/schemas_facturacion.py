from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

from schemas.schemas_user import UserCreate


class FacturaCreate(BaseModel):
    cliente_id: int
    productos: list[int]
    total: float

class FacturaResponse(BaseModel):
    id: int
    cliente_id: int
    productos: list[int]
    total: float

class Product_Register(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    reference: str = Field(..., min_length=1, max_length=20, description="Product reference")
    cost: float = Field(..., gt=0, description="Product cost")
    sale_price: float = Field(..., gt=0, description="Product sale price")
    profit_percentage: float = Field(..., ge=0, le=100, description="Profit percentage")
    quantity: int = Field(..., ge=1, description="Product quantity")
    distributor: str = Field(..., min_length=1, max_length=255, description="Distributor name")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Product Name",
                "reference": "Product Reference",
                "cost": 100.00,
                "sale_price": 150.00,
                "profit_percentage": 50.00,
                "quantity": 10,
                "distributor": "Distributor Name"
            }
        }

class Distributor_register(BaseModel):
    distributor_name: str = Field(..., min_length=1, max_length=255, description="Distributor name")
    distributor_nit: str = Field(..., min_length=1, max_length=50, description="Distributor NIT")
    contact_name: str = Field(..., min_length=1, max_length=255, description="Contact name")
    contact_phone: str = Field(..., min_length=1, max_length=50, description="Contact phone")
    contact_email: EmailStr = Field(..., description="Contact email")
    contact_name_accounting: str = Field(..., min_length=1, max_length=255, description="Accounting contact name")
    contact_phone_accounting: str = Field(..., min_length=1, max_length=50, description="Accounting contact phone")
    contact_email_accounting: EmailStr = Field(..., description="Accounting contact email")
    city_address: str = Field(..., min_length=1, max_length=255, description="City address")
    class Config:
        schema_extra: str = {
            "example": {
                "distributor_id": "123456",
                "distributor_name": "Distributor Name",
                "distributor_nit": "123456789",
                "contact_name": "Contact Name",
                "contact_phone": "1234567890",
                "contact_email": "contact@example.com",
                "contact_name_accounting": "Accounting Contact Name",
                "contact_phone_accounting": "0987654321",
                "contact_email_accounting": "accounting@example.com",
                "city_address": "City Address"
            }
        }


