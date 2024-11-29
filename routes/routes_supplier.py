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
