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
            "contact_user": "contact_name"
            }
        }

