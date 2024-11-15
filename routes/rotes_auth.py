from fastapi import APIRouter,FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from schemas.schemas_user import UserCreate, User, SupplierCreate, ProductCreate
from utils.crud import *
from utils.crud_db import *

from services.authentic import authenticate

from utils.connect import connect_db
import os
db = connect_db()

router_auth = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class Token(BaseModel):
    access_token: str
    token_type: str
    
    
@router_auth.post(path="/register_fy/",
    status_code=status.HTTP_200_OK,
    tags=['User'],
    #response_model = UserCreate,
    summary="""Register usuario.""")
async def register(user: UserCreate):
    db_user = query_user_exists(user.document) 
    if db_user["message"]:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_id = pwd_context.hash(user.document + user.email)
    user_obj = User(**user.dict(), user_id=user_id)
    
    """ Insert a new user into the users_ferroelectricos_yambitara table """
    sql = """INSERT INTO users_ferroelectricos_yambitara (user_id, password, email, document, name, type_document, contact_user, type_user)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
    hashed_password = pwd_context.hash(user.password)
    data = (user_obj.user_id, hashed_password, user_obj.email, user_obj.document, user_obj.name, user_obj.type_document, user_obj.contact_user, user_obj.type_user)
    user_id = query_db_insert(sql, data)
    return {"status": "ok", "message": "User created"}      

@router_auth.post("/login",
    status_code=status.HTTP_200_OK,
    tags=['User'],
    #response_model = UserCreate,
    summary="""Login usuario.""", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = query_user_exists_email(form_data.username)
    if not db_user["message"]:
        raise HTTPException(status_code=400, detail="Username not registered")
    token = authenticate(form_data.username, form_data.password)
    print(token)
    try:
        if not token:
            raise HTTPException(status_code=502, detail="Password incorrect")
        else:
            return {
                "access_token": token['access_token'],
                "token_type": "bearer"
            } 
            
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
@router_auth.post(path="/create_supplier/",
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
        
@router_auth.post(path="/create_product/",
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

        
@router_auth.delete(path="/delete_product/{product_id}/",
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

@router_auth.get(path="/get_products/",
    status_code=status.HTTP_200_OK,
    tags=['Product'],
    summary="""Get all products."""
)
async def get_products():
    sql = f"SELECT * FROM {os.getenv('DB_PRODUCT_TABLE')};"
    products = query_db(sql)
    return {"status": 200, "data": products}


#/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
