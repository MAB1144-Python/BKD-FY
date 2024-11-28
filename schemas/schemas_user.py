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

# class Distributor_register(BaseModel):
#     distributor_name: str = Field(..., min_length=1, max_length=255, description="Distributor name")
#     distributor_nit: str = Field(..., min_length=1, max_length=50, description="Distributor NIT")
#     contact_name: str = Field(..., min_length=1, max_length=255, description="Contact name")
#     contact_phone: str = Field(..., min_length=1, max_length=50, description="Contact phone")
#     contact_email: EmailStr = Field(..., description="Contact email")
#     contact_name_accounting: str = Field(..., min_length=1, max_length=255, description="Accounting contact name")
#     contact_phone_accounting: str = Field(..., min_length=1, max_length=50, description="Accounting contact phone")
#     contact_email_accounting: EmailStr = Field(..., description="Accounting contact email")
#     city_address: str = Field(..., min_length=1, max_length=255, description="City address")
#     class Config:
#         schema_extra: str = {
#             "example": {
#                 "distributor_id": "123456",
#                 "distributor_name": "Distributor Name",
#                 "distributor_nit": "123456789",
#                 "contact_name": "Contact Name",
#                 "contact_phone": "1234567890",
#                 "contact_email": "contact@example.com",
#                 "contact_name_accounting": "Accounting Contact Name",
#                 "contact_phone_accounting": "0987654321",
#                 "contact_email_accounting": "accounting@example.com",
#                 "city_address": "City Address"
#             }
#         }