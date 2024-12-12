from fastapi import HTTPException
from fastapi.responses import JSONResponse
from schemas.schemas_user import User
#from schemas.user_schema import UserBase
from core.security import get_password, verify_password #get_password, 
from typing import Optional,List
from fastapi.security import OAuth2PasswordBearer
from pydantic import  EmailStr
from typing import Union, Any

from dotenv import load_dotenv
import os

from uuid import uuid4

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from jose import jwt, JWTError
from datetime import datetime, timedelta
from email.mime.image import MIMEImage
from pydantic import  BaseSettings
from utils.config import load_config
import psycopg2

class Settings(BaseSettings):
    JWT_SECRET_KEY: str='JWT_SECRET_KEY'
    JWT_REFRESH_SECRET_KEY: str='JWT_REFRESH_SECRET_KEY'   
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    JWT_SECRET_KEY_ADMIN: str='JWT_SECRET_KEY_ADMIN'

settings = Settings()

def authenticate(email: str, password: str) -> Optional[User]:
    #try:
        variable_get_user_by_email = get_item_by_email(email)
        print("variable_get_user_by_email", variable_get_user_by_email)
        if variable_get_user_by_email["message"]:
                # si en el usuario se encuentra un @ significa que es un email 
                check_result_by_username=verify_password(password=password, hashed_pass=variable_get_user_by_email["password"])
                if check_result_by_username:
                    return {
                        "access_token": create_acess_token(email)
                    }
                else:
                    return {
                        "access_token_dont": "null"
                    }
        else:
            raise HTTPException(status_code=502, detail="Usuario no encontrado")
    # except:
    #     raise HTTPException(status_code=502, detail="Error en la autenticación")
    


def get_item_by_email(email):
    sql = f"SELECT user_id, password FROM {os.getenv('DB_USER_TABLE')} WHERE email = %s"
    user_data = None
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (email,))
                user_data = cur.fetchone()
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("presento el error ", error)
    
    if user_data:
        user_id, password = user_data
        return {"message": True, "user_id": user_id, "password": password}
    else:
        return {"message": False}
    


# def get_user_by_username(username:str, tabla_name):
    
#     table = Dynamodb.Table(str(os.getenv(tabla_name)))
#     """
#     description: Function that perfomed query over table of users by username,
#     this is used to validate the exist status

#     input: A username as a string
    
#     output: a json response from dynamoDB: response["Items"], typically a list
#     """
#     try:
#         response = table.query(
#             KeyConditionExpression = Key("username").eq(username)
#         )
#         return response["Items"]
#     except Exception:
#         raise HTTPException(status_code=404, detail="error to get data from database")
    
    
    
# def get_item_by_scan_dynamo(any_item_to_search:str,column_name_to_search:str, tabla_name)->List: 
#     """
#     description: Function to search by any_item_to_search in column_name_to_search of table_user of dynamoDB
#     input: an item to search as a atring and a column name to search as a atring
#     output: a JSON message.
#     """
#     table = Dynamodb.Table(str(os.getenv(tabla_name)))
#     try:
#         response = table.scan(
#             FilterExpression=Attr(column_name_to_search).eq(any_item_to_search)
#         ) 
#         return response["Items"]

#     except ClientError as e:
#         return JSONResponse(content=e.response["Error"], status_code=404)
    


# def get_email_by_username(username, tabla_name):
    
#     table = Dynamodb.Table(str(os.getenv(tabla_name)))
#     try:
#         query_params = {
#         'KeyConditionExpression': Key('username').eq(f'{username}')
#         }
#         response = table.query(**query_params)
#         return response['Items'][0][ATTRIBUTE_EMAIL_TABLE_USER]

#     except Exception as e:
#         print(e)
#         return os.getenv("DECODIFICATION_TOKEN_ERROR")


    


def create_acess_token(subject:Union[str, Any], expires_delta: int = None) -> str:
    """
    description: Function to create a JWT token with username, the token will expire after 60 minutes
    input: a username 
    output: a string with the token created with JWT token
    """
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow()+ timedelta(minutes = 60)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    enconded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm='HS256')
    return enconded_jwt