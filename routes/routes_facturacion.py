from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
#from models import Factura, Producto, Cliente
#from schemas.schemas_facturacion import FacturaCreate, FacturaResponse, Factura, Producto, Cliente
from schemas.schemas_user import UserCreate, User
from utils.crud import get_user_by_username, create_user, query_db_insert
from utils.config import load_config
from utils.crud_db import query_user_exists
import psycopg2
from fastapi import APIRouter,FastAPI, Depends, HTTPException, status
from passlib.context import CryptContext

from services.authentic import authenticate
from schemas.schemas_facturacion import Product_Register

from utils.connect import connect_db
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router_factura = APIRouter()

@router_factura.post(
        path="/create_product/",
        status_code=status.HTTP_201_CREATED,
        tags=['Product'],
        summary="""Create a new product."""
    )
async def create_product(producto: Product_Register):
        """ Insert a new product into the products table """
        sql = """INSERT INTO products (name, reference, cost, sale_price, profit_percentage, quantity, distributor)
                 VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        data = (producto.name, producto.reference, producto.cost, producto.sale_price, producto.profit_percentage, producto.quantity, producto.distributor)
        product_id = query_db_insert(sql, data)
        
        return {"status": "ok", "message": "Product created", "product_id": product_id}

@router_factura.post(
    path="/create_distributor/",
    status_code=status.HTTP_201_CREATED,
    tags=['User'],
    summary="""Create a new product and distributor."""
    )
async def create_distributor(distributor: dict):
    """ Insert a new distributor into the distributors table """
    sql_distributor = """INSERT INTO distributors (distributor_id, distributor_name, distributor_nit, contact_name, contact_phone, contact_email, contact_name_accounting, contact_phone_accounting, contact_email_accounting, city_address)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    data_distributor = (
        distributor['distributor_id'], distributor['distributor_name'], distributor['distributor_nit'], distributor.get('contact_name'),
        distributor.get('contact_phone'), distributor.get('contact_email'), distributor.get('contact_name_accounting'),
        distributor.get('contact_phone_accounting'), distributor.get('contact_email_accounting'), distributor.get('city_address')
    )
    distributor_id = query_db_insert(sql_distributor, data_distributor)
    
    return {"status": "ok", "message": "Product and distributor created", "product_id": product_id, "distributor_id": distributor_id}

# @router_factura.get("/consulta_db")
# def consulta_db(db: Session = Depends(get_db)):
#     try:
#         result = db.execute(text("SELECT 1")).fetchone()
#         return {"resultado": result[0]}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router_factura.post("/facturas/", response_model=FacturaResponse)
# def create_factura(factura: FacturaCreate, db: Session = Depends(get_db)):
#     return {"mensaje":"ok"}
#     db_factura = Factura(cliente_id=factura.cliente_id, total=factura.total)
#     db.add(db_factura)
#     db.commit()
#     db.refresh(db_factura)
#     for producto_id in factura.productos:
#         producto = db.query(Producto).filter(Producto.id == producto_id).first()
#         if not producto:
#             raise HTTPException(status_code=404, detail="Producto no encontrado")
#         db_factura.productos.append(producto)
#     db.commit()
#     return db_factura

# @router_factura.get("/facturas/{factura_id}", response_model=FacturaResponse)
# def read_factura(factura_id: int, db: Session = Depends(get_db)):
#     return {"mensaje":"ok"}
#     factura = db.query(Factura).filter(Factura.id == factura_id).first()
#     if factura is None:
#         raise HTTPException(status_code=404, detail="Factura no encontrada")
#     return factura

# @router_factura.get("/facturas/", response_model=list[FacturaResponse])
# def read_facturas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return {"mensaje":"ok"}
#     facturas = db.query(Factura).offset(skip).limit(limit).all()
#     return facturas

# @router_factura.delete("/facturas/{factura_id}", response_model=FacturaResponse)
# def delete_factura(factura_id: int, db: Session = Depends(get_db)):
#     return {"mensaje":"ok"}
#     factura = db.query(Factura).filter(Factura.id == factura_id).first()
#     if factura is None:
#         raise HTTPException(status_code=404, detail="Factura no encontrada")
#     db.delete(factura)
#     db.commit()
#     return factura


