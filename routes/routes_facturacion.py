from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.schemas_user import *
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
    db_user = query_user_exists_user_id(factura.user_id)
    if not db_user["message"]:
        raise HTTPException(status_code=200, detail="User not registered")
    db_seller = query_user_exists_user_id(factura.seller_id)
    if not db_seller["message"]:
        raise HTTPException(status_code=400, detail="Seller not registered")

    if db_seller["user_info"]["type_user"] not in ["seller", "online", "admin"]:
        raise HTTPException(status_code=400, detail="Seller unauthorized")

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
        data_sale_product = row.to_dict()
        db_product = query_product_exists_detail(data_sale_product["product_id"]) 
        if not db_product["message"]:
            raise HTTPException(status_code=400, detail="Product does not exist")
        # if data_sale_product["product_name"] != db_product["product_name"]:
        #     raise HTTPException(status_code=400, detail="Product name does not match")
        if data_sale_product["quantity_product"] > db_product['product_detail']["quantity"]:
            raise HTTPException(status_code=400, detail="Insufficient stock", product=db_product['product_detail']["quantity"])
        sql = """INSERT INTO sales_detail_ferroelectricos_yambitara (sale_id, sale_id_detail, product_id, product_name, quantity_product, cost_product, profit_product, discount_product, sale_product)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        sale_id_detail = pwd_context.hash(data_sale_product["sale_id"] + data_sale_product["product_id"] + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        data = (
            sale_id, sale_id_detail, data_sale_product["product_id"], data_sale_product["product_name"],
            data_sale_product["quantity_product"], data_sale_product["cost_product"], data_sale_product["profit_product"], data_sale_product["discount_product"], data_sale_product["sale_product"]
        )
        user_id = query_db_insert(sql, data)

        # Update the product quantity in the database
        new_quantity = db_product['product_detail']["quantity"] - data_sale_product["quantity_product"]
        update_sql = f"""UPDATE {os.getenv('DB_PRODUCT_TABLE')} SET quantity = %s WHERE product_id = %s;"""
        update_data = (new_quantity, data_sale_product["product_id"])
        query_db_insert(update_sql, update_data)
        
    sql = """INSERT INTO sales_ferroelectricos_yambitara (sale_id, id_sale_dian, user_id, seller_id, sale_cost, sale_discount, sale_profit, sale_total)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
    id_sale_dian = pwd_context.hash("id_sale_dian_test"+ datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    sale_cost = df["cost_product"].sum()
    sale_discount = df["discount_product"].sum()
    sale_profit = df["profit_product"].sum()
    sale_total = df["sale_product"].sum()
    
    data = (
        sale_id, id_sale_dian, factura.user_id, factura.seller_id,
        float(sale_cost), float(sale_discount), float(sale_profit), float(sale_total))
    user_id = query_db_insert(sql, data)
    raise HTTPException(status_code=200, detail="Bill register")   

@router_factura.get("/sales_details/", 
    status_code=status.HTTP_200_OK,
    tags=['Bill'],
    summary="""Get all sales details.""")
async def get_all_sales_details():
    sql = f"SELECT * FROM {os.getenv('DB_SALE_TABLE_DETAIL')};"
    sales_details = query_db(sql)
    if not sales_details:
        raise HTTPException(status_code=404, detail="No sales details found")
    return HTTPException(status_code=200, detail= {"data": sales_details})

@router_factura.get("/bills_registered/", 
    status_code=status.HTTP_200_OK,
    tags=['Bill'],
    summary="""Get all bills.""")
async def get_all_bills():
    sql = f"SELECT * FROM {os.getenv('DB_SALE_TABLE')};"
    bills = query_db(sql)
    if not bills:
        raise HTTPException(status_code=404, detail="No bills found")
    return HTTPException(status_code=200, detail= {"data": bills})
