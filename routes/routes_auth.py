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
    db_user = query_user_exists(user.document) 
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
    print(db_user)
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



#/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
