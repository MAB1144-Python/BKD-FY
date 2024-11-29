from fastapi import APIRouter,FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from schemas.schemas_user import *
from schemas.schemas_facturacion import *
from utils.crud_db import *

from services.authentic import authenticate


router_supplier = APIRouter()

@router_supplier.post(path="/create_supplier/",
    status_code=status.HTTP_201_CREATED,
    tags=['Supplier'],
    summary="""Create a new supplier."""
)
async def create_supplier(supplier: SupplierCreate):
    db_user = query_user_exists_supplier(supplier.supplier_nit)
    if db_user["message"]:
        raise HTTPException(status_code=400, detail="Username already registered")
    """ Insert a new supplier into the suppliers_ferroelectricos_yambitara table """
    sql_supplier = """INSERT INTO suppliers_ferroelectricos_yambitara (supplier_id, supplier_nit, supplier_name, supplier_contact_name, supplier_contact_email, supplier_contact_contable, supplier_phone, supplier_phone_two, supplier_address)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    supplier_id = pwd_context.hash(supplier.supplier_nit + supplier.supplier_name)
    data_supplier = (
        supplier_id, supplier.supplier_nit, supplier.supplier_name, supplier.supplier_contact_name,
        supplier.supplier_contact_email, supplier.supplier_contact_contable, supplier.supplier_phone,
        supplier.supplier_phone_two, supplier.supplier_address
    )
    supplier_id = query_db_insert(sql_supplier, data_supplier)
    
    return {"status": 200, "message": "Supplier created"}

@router_supplier.put(path="/update_supplier/",
    status_code=status.HTTP_200_OK,
    tags=['Supplier'],
    summary="""Update an existing supplier."""
)
async def update_supplier(supplier: SupplierCreate):
    db_user = query_user_exists_supplier(supplier.supplier_nit)
    if not db_user["message"]:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    """ Retrieve supplier_id from suppliers_ferroelectricos_yambitara table by supplier_nit """
    sql_supplier = """SELECT supplier_id FROM suppliers_ferroelectricos_yambitara WHERE supplier_nit = %s;"""
    supplier_id = query_db_fetchone(sql_supplier, (supplier.supplier_nit,))
    if not supplier_id:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    """ Update an existing supplier in the suppliers_ferroelectricos_yambitara table """
    sql_supplier = """UPDATE suppliers_ferroelectricos_yambitara 
                      SET supplier_nit = %s, supplier_name = %s, supplier_contact_name = %s, 
                          supplier_contact_email = %s, supplier_contact_contable = %s, 
                          supplier_phone = %s, supplier_phone_two = %s, supplier_address = %s
                      WHERE supplier_id = %s;"""
    data_supplier = (
        supplier.supplier_nit, supplier.supplier_name, supplier.supplier_contact_name,
        supplier.supplier_contact_email, supplier.supplier_contact_contable, supplier.supplier_phone,
        supplier.supplier_phone_two, supplier.supplier_address, supplier_id["message"]
    )
    query_db_insert(sql_supplier, data_supplier)
    
    return {"status": 200, "message": "Supplier updated"}

@router_supplier.post(path="/get_supplier_id/",
    status_code=status.HTTP_200_OK,
    tags=['Supplier'],
    summary="""Get supplier ID by NIT."""
)
async def get_supplier_id(supplier_nit: str):
    """ Retrieve supplier_id from suppliers_ferroelectricos_yambitara table by supplier_nit """
    sql_supplier = """SELECT supplier_id FROM suppliers_ferroelectricos_yambitara WHERE supplier_nit = %s;"""
    supplier_id = query_db_fetchone(sql_supplier, (supplier_nit,))
    if not supplier_id:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    return {"supplier_id": supplier_id["message"][0]}

@router_supplier.get(path="/get_all_suppliers/",
    status_code=status.HTTP_200_OK,
    tags=['Supplier'],
    summary="""Get all suppliers without supplier_id."""
)
async def get_all_suppliers():
    """ Retrieve all suppliers from suppliers_ferroelectricos_yambitara table without supplier_id """
    sql_suppliers = """SELECT supplier_nit, supplier_name, supplier_contact_name, supplier_contact_email, 
                                supplier_contact_contable, supplier_phone, supplier_phone_two, supplier_address 
                        FROM suppliers_ferroelectricos_yambitara;"""
    suppliers = query_db_fetchall(sql_suppliers)
    if not suppliers:
        raise HTTPException(status_code=404, detail="No suppliers found")
    return {"suppliers": suppliers["message"]}

