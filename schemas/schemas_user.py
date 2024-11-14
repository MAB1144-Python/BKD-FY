from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field, EmailStr
from uuid import uuid4
from datetime import datetime


def generate_id():
    return str(uuid4())

def generate_date():
    return str(datetime.now())

Base = declarative_base()

# class User(Base):
#     __tablename__ = 'users'
    
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)

class UserCreate(BaseModel):
    document: str = Field(..., description="document", max_length=50)
    name: str = Field(..., description="name", max_length=50)
    email: EmailStr = Field(..., description="user email")
    password: str = Field(..., min_length=8, max_length=25, description="password")
    type_document: str = Field(..., description="type of document", max_length=50)
    type_user: str = Field(..., description="type of user", max_length=50)
    contact_user: str = Field(..., description="contact user", max_length=100)
    created_at: str = Field(default_factory=generate_date)
    class Config:
        schema_extra = {
            "example": {
            "document": "123456789",
            "name": "your_name",
            "email": "test@gmail.com",
            "password": "123456789",
            "type_document": "passport",
            "type_user": "admin",
            "contact_user": "contact_name"
            }
        }

class User(BaseModel):
    user_id: str = Field(default_factory="user_default", description="user_id")
    document: str = Field(..., description="document", max_length=50)
    name: str = Field(..., description="name", max_length=50)
    email: EmailStr = Field(..., description="user email")
    password: str = Field(..., min_length=8, max_length=25, description="password")
    type_document: str = Field(..., description="type of document", max_length=50)
    type_user: str = Field(..., description="type of user", max_length=50)
    contact_user: str = Field(..., description="contact user", max_length=100)
    created_at: str = Field(default_factory=generate_date)
    class Config:
        schema_extra = {
            "example": {
            "document": "123456789",
            "name": "your_name",
            "email": "test@gmail.com",
            "password": "123456789",
            "type_document": "passport",
            "type_user": "admin",
            "contact_user": "contact_name"
            }
        }


class SupplierCreate(BaseModel):
    supplier_nit: str = Field(..., description="Supplier NIT", max_length=50)
    supplier_name: str = Field(..., description="Supplier Name", max_length=100)
    supplier_contact_name: str = Field(None, description="Contact Name", max_length=100)
    supplier_contact_email: EmailStr = Field(None, description="Contact Email")
    supplier_contact_contable: str = Field(None, description="Contact Contable", max_length=100)
    supplier_phone: str = Field(None, description="Phone", max_length=20)
    supplier_phone_two: str = Field(None, description="Phone Two", max_length=20)
    supplier_address: str = Field(None, description="Address")

    class Config:
        schema_extra = {
            "example": {
                "supplier_nit": "123456789",
                "supplier_name": "Supplier Name",
                "contact_name": "Contact Name",
                "contact_email": "contact@example.com",
                "contact_contable": "Contact Contable",
                "phone": "1234567890",
                "phone_two": "0987654321",
                "address": "123 Supplier St.",
            }
        }

class ProductCreate(BaseModel):
    product_name: str = Field(..., description="Product Name", max_length=100)
    cost_products: str = Field(..., description="Cost of products", example="100.00")
    sale_price: str = Field(..., description="Sale price", example="150.00")
    quantity: int = Field(..., description="Quantity", example=10)
    suppliers: str = Field(..., description="Suppliers", max_length=100, example="Supplier Name")
    description_products: str = Field(None, description="Description of products", example="A detailed description")
    profit_margin: str = Field(..., description="Profit margin", example="50.00")
    image_reference: str = Field(None, description="Image reference", example="image_url")
    class Config:
        schema_extra = {
            "example": {
                "product_name": "Product Name",
                "cost_products": 100.00,
                "sale_price": 150.00,
                "quantity": 10,
                "suppliers": "Supplier Name",
                "description_products": "A detailed description",
                "profit_margin": 50.00,
                "image_reference": "image_url",
            }
        }