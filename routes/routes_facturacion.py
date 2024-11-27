from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.schemas_user import *
from utils.crud import get_user_by_username, create_user, query_db_insert
from utils.config import load_config
from utils.crud_db import *
import psycopg2
from fastapi import APIRouter,FastAPI, Depends, HTTPException, status
from passlib.context import CryptContext

from services.authentic import authenticate
from schemas.schemas_facturacion import *

from utils.connect import connect_db
import os
import pandas as pd

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router_factura = APIRouter()

@router_factura.post("/bill/", 
    status_code=status.HTTP_200_OK,
    tags=['Bill'],
    # response_model=FacturaResponse
    summary="""Register bill.""")
async def create_factura(factura: FacturaCreate):
    df = pd.DataFrame([], columns=[
        "sale_id",
        "id_sale_dian",
        "user_id",
        "seller_id",
        "product_id", 
        "product_name", 
        "quantity_product", 
        "cost_product",
        "profit_product",
        "discount_product", 
        "sale_product"
    ])
    print(datetime.now())
    sale_id = pwd_context.hash(factura.user_id + factura.seller_id + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    id_sale_dian = pwd_context.hash("id_sale_dian_test"+ datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for producto in factura.productos:
        cost_product = 0
        profit_product = 0
        new_row = {
            "sale_id": sale_id,
            "id_sale_dian": id_sale_dian,
            "user_id": factura.user_id,
            "seller_id": factura.seller_id,
            "product_id": producto["product_id"],
            "product_name": producto["product_name"],
            "quantity_product": producto["quantity_product"],
            "cost_product": cost_product,
            "profit_product": profit_product,
            "discount_product": producto["discount_product"],
            "sale_product": producto["sale_product"]
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    for index, row in df.iterrows():
        db_product = query_product_exists(row["product_id"]) 
        if db_product["message"]:
            raise HTTPException(status_code=400, detail="Product does not exist")
        if row["product_name"] != db_product["product_name"]:
            raise HTTPException(status_code=400, detail="Product name does not match")
        # if row["quantity_product"] > db_product["quantity"]:
        #     raise HTTPException(status_code=400, detail="Insufficient stock")
        
        sql = """INSERT INTO productos_facturacion (sale_id, id_sale_dian, user_id, seller_id, product_id, product_name, quantity_product, cost_product, profit_product, discount_product, sale_product)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        data = (
            row["sale_id"], row["id_sale_dian"], row["user_id"], row["seller_id"], row["product_id"], row["product_name"],
            row["quantity_product"], row["cost_product"], row["profit_product"], row["discount_product"], row["sale_product"]
        )
        user_id = query_db_insert(sql, data)
    raise HTTPException(status_code=200, detail="Bill register")   


@router_factura.get("/bills_registered/", 
    status_code=status.HTTP_200_OK,
    tags=['Bill'],
    summary="""Get all bills.""")
async def get_all_bills():
    sql = f"SELECT * FROM {os.getenv('DB_SALE_TABLE')};"
    print(sql)
    bills = query_db(sql)
    if not bills:
        raise HTTPException(status_code=404, detail="No bills found")
    return bills
