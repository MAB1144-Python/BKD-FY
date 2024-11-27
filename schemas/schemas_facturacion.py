from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

from schemas.schemas_user import UserCreate



class FacturaResponse(BaseModel):
    id: int
    cliente_id: int
    productos: list[int]
    total: float

# class Product_Register(BaseModel):
#     name: str = Field(..., min_length=1, max_length=255, description="Product name")
#     reference: str = Field(..., min_length=1, max_length=20, description="Product reference")
#     cost: float = Field(..., gt=0, description="Product cost")
#     sale_price: float = Field(..., gt=0, description="Product sale price")
#     profit_percentage: float = Field(..., ge=0, le=100, description="Profit percentage")
#     quantity: int = Field(..., ge=1, description="Product quantity")
#     distributor: str = Field(..., min_length=1, max_length=255, description="Distributor name")
    
#     class Config:
#         schema_extra = {
#             "example": {
#                 "name": "Product Name",
#                 "reference": "Product Reference",
#                 "cost": 100.00,
#                 "sale_price": 150.00,
#                 "profit_percentage": 50.00,
#                 "quantity": 10,
#                 "distributor": "Distributor Name"
#             }
#         }


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


class ProductUpdate(BaseModel):
    product_id: str = Field(..., description="Product ID", example="p1")
    product_name: str = Field(..., description="Product Name", max_length=100)
    cost_products: float = Field(..., description="Cost of products", example=100.00)
    sale_price: float = Field(..., description="Sale price", example=150.00)
    quantity: float = Field(..., description="Quantity", example=10)
    suppliers: str = Field(..., description="Suppliers", max_length=100, example="Supplier Name")
    description_products: str = Field(None, description="Description of products", example="A detailed description")
    profit_margin: float = Field(..., description="Profit margin", example=50.00)
    image_reference: str = Field(None, description="Image reference", example="image_url")
    class Config:
        schema_extra = {
            "example": {
                "product_id": "p1",
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



class FacturaCreate(BaseModel):
    user_id: str = Field(..., description="ID del cliente")
    seller_id: str = Field(..., description="ID del vendedor")
    productos: list[dict] = Field(..., description="Lista de productos con detalles")
    class Config:
        schema_extra = {
            "example": {
            "user_id": "user_123",
            "seller_id": "seller_123",
            "productos": [
                {
                "product_id": "p1",
                "product_name": "Product A",
                "quantity_product": 2,
                "discount_product": 5.00,
                "sale_product": 90.00
                },
                {
                "product_id": "p2",
                "product_name": "Product B",
                "quantity_product": 1,
                "discount_product": 0.00,
                "sale_product": 150.00
                }
            ]
            }
        }

