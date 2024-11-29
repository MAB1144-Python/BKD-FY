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



router_user = APIRouter()