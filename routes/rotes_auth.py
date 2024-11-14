from fastapi import APIRouter,FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from schemas.schemas_user import UserCreate, User
from utils.crud import get_user_by_username, create_user, query_db_insert
from utils.crud_db import query_user_exists, query_user_exists_email

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

@router_auth.post(    
    path="/register_fy/",
    status_code=status.HTTP_200_OK,
    tags=['User'],
    #response_model = UserCreate,
    summary="""Register usuario.""")
async def register(user: UserCreate):
    db_user = query_user_exists(user.document) #get_user_by_username(db, document=user.document)
    if db_user["message"]:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_id = pwd_context.hash(user.document + user.email)
    user_obj = User(**user.dict(), user_id=user_id)
    
    """ Insert a new user into the users_ferroelectricos_yambitara table """
    sql = """INSERT INTO users_ferroelectricos_yambitara (user_id, password, email, document, name, type_document, contact_user)
                VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    hashed_password = pwd_context.hash(user.password)
    #data = (user.user_id, hashed_password, user.email, user.document, user.name, user.type_document, user.contact_user)
    data = (user_obj.user_id, hashed_password, user_obj.email, user_obj.document, user_obj.name, user_obj.type_document, user_obj.contact_user)
    user_id = query_db_insert(sql, data)
     
    return {"status": "ok", "message": "User created"}      


@router_auth.post("/login",
    status_code=status.HTTP_200_OK,
    tags=['User'],
    #response_model = UserCreate,
    summary="""Register usuario.""", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = query_user_exists_email(form_data.username)
    if not db_user["message"]:
        raise HTTPException(status_code=400, detail="Username not registered")
    token = authenticate(form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return {
            "access_token": token['access_token'],
            "token_type": "bearer"
        } 


#/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
