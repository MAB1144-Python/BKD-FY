from fastapi import APIRouter,FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from schemas.schemas_user import *
from schemas.schemas_facturacion import *
from utils.crud_db import *

from services.authentic import authenticate


router_auth = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class Token(BaseModel):
    access_token: str
    token_type: str
    
    
@router_auth.post(path="/register_fy/",
    status_code=status.HTTP_200_OK,
    tags=['Auth'],
    #response_model = UserCreate,
    summary="""Register usuario.""")
async def register(user: UserCreate):
    hashed_password = pwd_context.hash(user.password)    
    db_user = query_user_exists_email(user.email) 
    if db_user["message"]:
        raise HTTPException(status_code=400, detail="email already registered")
    
    db_user = query_user_exists_document(user.document)
    if db_user["message"]:
        raise HTTPException(status_code=400, detail="document already registered")
    
    user_id = pwd_context.hash(user.document + user.email)
    user_obj = User(**user.dict(), user_id=user_id)
    
    """ Insert a new user into the users_ferroelectricos_yambitara table """
    sql = """INSERT INTO users_ferroelectricos_yambitara (user_id, password, email, document, name, type_document, contact_user, type_user)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
    hashed_password = pwd_context.hash(user.password)
    data = (user_obj.user_id, hashed_password, user_obj.email, user_obj.document, user_obj.name, user_obj.type_document, user_obj.contact_user, user_obj.type_user)
    
    user_id = query_db_insert(sql, data)
    raise HTTPException(status_code=200, detail="User created")    

@router_auth.post("/login",
    status_code=status.HTTP_200_OK,
    tags=['Auth'],
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
   
   
@router_auth.get("/users",
    status_code=status.HTTP_200_OK,
    tags=['Auth'],
    summary="""Get all registered users.""")
async def get_users():
    users = get_all_users()
    return users

@router_auth.post("/user_info/",
    status_code=status.HTTP_200_OK,
    tags=['Auth'],
    summary="""Get user by email.""")
async def get_user_by_email(email: str):
    db_user = query_user_exists_email(email)
    if not db_user["message"]:
        raise HTTPException(status_code=400, detail="User not registered")
    """ Retrieve user information from the users_ferroelectricos_yambitara table """
    sql = """SELECT email, document, name, type_document, contact_user, type_user
             FROM users_ferroelectricos_yambitara WHERE email = %s;"""
    data = (email,)
    db_user = query_db_fetchone(sql, data)
    if not db_user:
        raise HTTPException(status_code=404, detail="User information not found")
    return {
        "email": db_user["message"][0],
        "document": db_user["message"][1],
        "name": db_user["message"][2],
        "type_document": db_user["message"][3],
        "contact_user": db_user["message"][4],
        "type_user": db_user["message"][5],
    }

@router_auth.put("/update_user_info/",
    status_code=status.HTTP_200_OK,
    tags=['Auth'],
    summary="""Update user information.""")
async def update_user_info(user: UserUpdate):
    db_user = query_user_exists_document(user.document)
    if not db_user["message"]:
        raise HTTPException(status_code=404, detail="User not found")
    
    """ Update user information in the users_ferroelectricos_yambitara table """
    sql = """UPDATE users_ferroelectricos_yambitara 
             SET email = %s, name = %s, type_document = %s, contact_user = %s
             WHERE document = %s;"""
    data = (user.email, user.name, user.type_document, user.contact_user, user.document)
    
    query_db_update(sql, data)
    return {"detail": "User information updated successfully"}

@router_auth.put("/update_user_type/",
    status_code=status.HTTP_200_OK,
    tags=['Auth'],
    summary="""Update user type.""")
async def update_user_type(document: str, new_type_user: str, admin_email: str, admin_password: str):
    # Verify admin credentials
    admin_user = query_user_is_admin(admin_email)
    if not admin_user["message"]:
        raise HTTPException(status_code=400, detail="Admin email not registered")
    
    token = authenticate(admin_email, admin_password)
    if not token:
        raise HTTPException(status_code=401, detail="Admin password incorrect")
    
    # Verify user existence
    db_user = query_user_exists_document(document)
    if not db_user["message"]:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user type
    sql = """UPDATE users_ferroelectricos_yambitara 
                SET type_user = %s
                WHERE document = %s;"""
    data = (new_type_user, document)
    
    query_db_update(sql, data)
    return {"detail": "User type updated successfully"}
    
@router_auth.get("/user_types",
    status_code=status.HTTP_200_OK,
    tags=['Auth'],
    summary="""Get user types.""")
async def get_user_types():
    user_types = ["admin", "user", "seller"]
    return {"user_types": user_types}

#/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
