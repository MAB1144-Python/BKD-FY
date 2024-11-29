from fastapi import APIRouter,FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from schemas.schemas_user import *
from schemas.schemas_facturacion import *
from utils.crud import *
from utils.crud_db import *

from services.authentic import authenticate

from utils.connect import connect_db
import os


router_product = APIRouter()

@router_product.post(path="/create_product/",
    status_code=status.HTTP_201_CREATED,
    tags=['Product'],
    summary="""Create a new product."""
)
async def create_product(product: ProductCreate):
    db_user = query_user_exists_products(product.product_name)
    print(db_user)
    if db_user["message"]:
        raise HTTPException(status_code=400, detail="Product already registered")
    """ Insert a new product into the products_ferroelectricos_yambitara table """
    sql_product = f"""INSERT INTO {os.getenv('DB_PRODUCT_TABLE')} (product_id, product_name, cost_products, sale_price, quantity, suppliers, description_products, profit_margin, image_reference)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    product_id = pwd_context.hash(product.product_name)
    data_product = (
        product_id,product.product_name, product.cost_products, product.sale_price, product.quantity, product.suppliers,
        product.description_products, product.profit_margin, product.image_reference
    )
    product_result = query_db_insert(sql_product, data_product)
    
    return {"status": 200, "message": "Product created"}
        
@router_product.put(path="/update_product/",
    status_code=status.HTTP_200_OK,
    tags=['Product'],
    summary="""Update an existing product."""
)
async def update_product(product: ProductUpdate):
    db_product = query_user_exists_products_id(product.product_id)
    if db_product["message"]:
        raise HTTPException(status_code=400, detail="Product not found")
    
    """ Update an existing product in the products_ferroelectricos_yambitara table """
    sql_product = f"""UPDATE {os.getenv('DB_PRODUCT_TABLE')} 
                      SET product_name = %s, cost_products = %s, sale_price = %s, quantity = %s, suppliers = %s, 
                          description_products = %s, profit_margin = %s, image_reference = %s
                      WHERE product_id = %s;"""
    data_product = (
        product.product_name, product.cost_products, product.sale_price, product.quantity, product.suppliers,
        product.description_products, product.profit_margin, product.image_reference, product.product_id
    )
    result = query_db_update(sql_product, data_product)
    
    if result:
        return {"status": 200, "message": "Product updated"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@router_product.put(path="/update_product_quantity/",
    status_code=status.HTTP_200_OK,
    tags=['Product'],
    summary="""Update the quantity of an existing product."""
)
async def update_product_quantity(product_id: str, quantity: int):
    db_product = query_user_exists_products_id(product_id)
    if db_product["message"]:
        raise HTTPException(status_code=400, detail="Product not found")
    
    """ Update the quantity of an existing product in the products_ferroelectricos_yambitara table """
    sql_product = f"""UPDATE {os.getenv('DB_PRODUCT_TABLE')} 
                        SET quantity = %s
                        WHERE product_id = %s;"""
    data_product = (quantity, product_id)
    result = query_db_update(sql_product, data_product)
    
    if result:
        return {"status": 200, "message": "Product quantity updated"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@router_product.delete(path="/delete_product/",
    status_code=status.HTTP_200_OK,
    tags=['Product'],
    summary="""Delete a product."""
)
async def delete_product(product_id: str):
    db_product = query_user_exists_products_id(product_id)
    print(db_product)
    if db_product["message"]:
        raise HTTPException(status_code=400, detail="Product not found")

    """ Delete a product from the products_ferroelectricos_yambitara table """
    sql_product = f"DELETE FROM {os.getenv('DB_PRODUCT_TABLE')} WHERE product_id = %s;"
    data_product = (product_id,)
    result = query_db_delete(sql_product, data_product)
    
    if result:
        return {"status": 200, "message": "Product deleted"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@router_product.get(path="/get_products/",
    status_code=status.HTTP_200_OK,
    tags=['Product'],
    summary="""Get all products."""
)
async def get_products():
    sql = f"SELECT * FROM {os.getenv('DB_PRODUCT_TABLE')};"
    products = query_db(sql)
    return {"status": 200, "data": products}

