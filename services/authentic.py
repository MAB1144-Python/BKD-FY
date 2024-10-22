import pandas as pd
from botocore.exceptions import ClientError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key, Attr
from schemas.user import User,UserAuth
#from schemas.user_schema import UserBase
from core.security import get_password, verify_password #get_password, 
from typing import Optional,List
from utils.connection_keys import load_dymano_table
from fastapi.security import OAuth2PasswordBearer
from pydantic import  EmailStr
from typing import Union, Any

from boto3 import resource
from dotenv import load_dotenv
import os
import boto3

from uuid import uuid4

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from jose import jwt, JWTError
from datetime import datetime, timedelta
from utils.connection_keys import load_dynamoclient
from email.mime.image import MIMEImage
from pydantic import  BaseSettings


Dynamodb = resource("dynamodb",
                    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                    region_name=os.getenv("REGION_NAME"))
dynamodb_client = boto3.client('dynamodb', 
                    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                    region_name=os.getenv("REGION_NAME"))

ATTRIBUTE_FIRST_NAME_TABLE_USER='first_name'
ATTRIBUTE_IS_VERIFIED_TABLE_USERS='is_verified'
ATTRIBUTE_EMAIL_TABLE_USER="email"


class Settings(BaseSettings):

    JWT_SECRET_KEY: str='JWT_SECRET_KEY'
    JWT_REFRESH_SECRET_KEY: str='JWT_REFRESH_SECRET_KEY'   
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    JWT_SECRET_KEY_ADMIN: str='JWT_SECRET_KEY_ADMIN'

settings = Settings()

def authenticate(email: str, password: str, tabla_name:str) -> Optional[User]:
    """
    description: Function to authenticate the user in the form of page of login and password
    input: a email and password as a string
    output: Optional a object type User
    """
    try:
        variable_get_user_by_email = get_item_by_email(email , tabla_name)

        if len(variable_get_user_by_email) == 1:
                # si en el usuario se encuentra un @ significa que es un email 
                print(password)
                print("second ",variable_get_user_by_email["password"].values[0])
                check_result_by_username=verify_password(password=password, hashed_pass=variable_get_user_by_email["password"].values[0])
                if check_result_by_username:
                    return {
                        "access_token": create_acess_token(email)
                    }
                else:
                    raise HTTPException(status_code=502, detail="Password incorrect")
        else:
            raise HTTPException(status_code=502, detail="Usuario no encontrado")
    except:
        raise HTTPException(status_code=502, detail="Error en la autenticación")
    
    
    check_result_by_username=verify_password(password=password, hashed_pass=variable_get_user_by_username[0]["password"])
    print("authentic 61 ",check_result_by_username)
    try:
        check_result_by_username=verify_password(password=password, hashed_pass=variable_get_user_by_username[0]["password"])
    except Exception:
        check_result_by_username=False
    try:
        result_of_check_with_email=verify_password(password=password, hashed_pass=variable_get_user_by_email[0]["password"])
    except Exception:
         result_of_check_with_email=False
    if check_result_by_username:
        return variable_get_user_by_username
    elif result_of_check_with_email:
        return variable_get_user_by_email
    else:
        return None
    


def get_user_by_username(username:str, tabla_name):
    
    table = Dynamodb.Table(str(os.getenv(tabla_name)))
    """
    description: Function that perfomed query over table of users by username,
    this is used to validate the exist status

    input: A username as a string
    
    output: a json response from dynamoDB: response["Items"], typically a list
    """
    try:
        response = table.query(
            KeyConditionExpression = Key("username").eq(username)
        )
        return response["Items"]
    except Exception:
        raise HTTPException(status_code=404, detail="error to get data from database")
    
    
    
def get_item_by_scan_dynamo(any_item_to_search:str,column_name_to_search:str, tabla_name)->List: 
    """
    description: Function to search by any_item_to_search in column_name_to_search of table_user of dynamoDB
    input: an item to search as a atring and a column name to search as a atring
    output: a JSON message.
    """
    table = Dynamodb.Table(str(os.getenv(tabla_name)))
    try:
        response = table.scan(
            FilterExpression=Attr(column_name_to_search).eq(any_item_to_search)
        ) 
        return response["Items"]

    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=404)
    


def get_email_by_username(username, tabla_name):
    
    table = Dynamodb.Table(str(os.getenv(tabla_name)))
    try:
        query_params = {
        'KeyConditionExpression': Key('username').eq(f'{username}')
        }
        response = table.query(**query_params)
        return response['Items'][0][ATTRIBUTE_EMAIL_TABLE_USER]

    except Exception as e:
        print(e)
        return os.getenv("DECODIFICATION_TOKEN_ERROR")


def get_item_by_email(email, tabla_name):
    table_client = load_dymano_table(tabla_name)
    response = table_client.scan()
    data = response['Items']
    print(tabla_name)
    print(data)
    df_data = pd.DataFrame.from_dict(data)
    return df_data[df_data["email"]==email]
    


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