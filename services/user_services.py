import pandas as pd
from botocore.exceptions import ClientError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key, Attr
from schemas.user import User,UserAuth,Token
#from schemas.user_schema import UserBase
from utils.connection_keys import load_dymano_table
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from pydantic import  EmailStr

from boto3 import resource
from dotenv import load_dotenv
import os
from uuid import uuid4

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from jose import jwt, JWTError
from datetime import datetime, timedelta
from utils.connection_keys import load_dynamoclient
from email.mime.image import MIMEImage

load_dotenv()

ATTRIBUTE_CREDITS_TABLE_USER='credits'
ATTRIBUTE_FIRST_NAME_TABLE_USER='first_name'

ATTRIBUTE_IS_VERIFIED_TABLE_USERS='is_verified'
ATTRIBUTE_EMAIL_TABLE_USER="email"


JWT_SECRET_TOKEN_EMAIL = os.getenv("SECRET_KEY_EMAIL")
JWT_ALGORITHM_TOKEN_EMAIL= os.getenv("ALGORITHM_CIPER_EMAIL")
JWT_EXPIRATION_TIME_MINUTES_TOKEN_EMAIL= os.getenv("JWT_EXPIRATION_TIME_MINUTES_TOKEN_EMAIL_TIME")


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name="JWT"
)

# dynamodb = resource("dynamodb",
#                     aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
#                     aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
#                     region_name=os.getenv("REGION_NAME"))

# table = dynamodb.Table(os.getenv("TABLE_USER"))
# tableModelConfig = dynamodb.Table(os.getenv("AAAS_MODEL_CONFIG"))




# def generate_id():
#     return str(uuid4())

# def get_user_by_email(email:EmailStr) -> Optional[User]: 
#     try:
#         response = table.scan(
#             TableName=os.getenv("TABLE_USER"),
#             FilterExpression=Attr('email').eq(email)
#         ) 
#         return response["Items"]

#     except ClientError as e:
#         return JSONResponse(content=e.response["Error"], status_code=404)
    



# def create_user(user : UserAuth):
#     user_validate = get_user_by_username(username=user.username)
#     email_user_validation = get_user_by_email(email=user.email)

#     if ((not user_validate) and (not email_user_validation)):
#         try:
#             user_in=UserAuth(
#                 first_name = user.first_name,
#                 last_name = user.last_name,
#                 email = user.email,
#                 username = user.username,
#                 born_date = user.born_date,
#                 password = get_password(user.password),
#                 credits=100,
#                 is_verified=False        
#             )
#             aDict = vars(user_in)
#             table.put_item(Item=aDict)
#             verification_code_jwt=generate_token(user.username)
#             send_email_with_verification_code(user.email,verification_code_jwt)

#             return JSONResponse(status_code=201, content={"message": "registered successfully"})
#         except ClientError as e:
#             return JSONResponse(content=e.response["User with this email or username already exists"], status_code=500)
#     else:
#         return JSONResponse(status_code=409, content={"message": "User with this email or username already exists"})
    
 



def authenticate(email: str, password: str) -> Optional[User]:
    user = get_user_by_username(email=email)
    if not user:
        return None
    if not verify_password(password=password, hashed_pass=user[0]["password"]):
        return None
    return user





def get_user_by_username(username:str) -> Optional[User]:
    table_user = load_dymano_table("user_bubble_cat")
    response = table_user.query(
        KeyConditionExpression = Key("username").eq(username)
    )
    print("response...............",response["Items"])
    return response["Items"]





def verify_id(id:str):
    try:
        response = table.scan(
            TableName=os.getenv("TABLE_USER"),
            FilterExpression=Attr('user_id').eq(id)
        ) 
        if len(response["Items"]) == 0:
            return False
        else:
            return True
        
    except ClientError as e:
        return False
    


def get_users():
    try:
        response = table.scan(
            AttributesToGet = ["username","created_at", "cellphone","first_name", "last_name", "email", "user_id", "born_date"]
        )
        return response["Items"]

    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)




def delete_user(user:dict):
    try:
        response=table.delete_item(
            Key = {
                    "username":user['username'], 
                    "created_at":user["created_at"]
            }
        )
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    


    

# def update_user(user:UserBase,username,create_at):
#     try:
#         response = table.update_item(
#             Key = {
#                     "username":username, 
#                     "created_at":create_at
#             },
#             UpdateExpression = "SET first_name = :first_name, last_name = :last_name, email=:email, cellphone=:cellphone, born_date=:born_date",
#             ExpressionAttributeValues ={
#                 ":first_name": user.first_name,
#                 ":last_name": user.last_name,
#                 ":email": user.email,
#                 ":cellphone": user.cellphone,
#                 ":born_date": user.born_date},
#             ReturnValues="UPDATED_NEW")
#         return response
#     except ClientError as e:
#         return JSONResponse(content=e.response["Error"], status_code=500)
    



def updated_user_v2(username):
    query_params = {
    'KeyConditionExpression': Key(os.getenv("PARTITION_KEY_TABLE_USER")).eq(f'{username}')
    }
    response = table.query(**query_params)
    print(response)

 
    


def calculate_cost_of_usage_models(models_dict):
    table = dynamodb.Table(os.getenv("MODEL_CONFIG"))
    total_cost=0
    for key, value in models_dict.items():
        query_params = {
            'KeyConditionExpression': Key('model_id').eq(f'{key}')
        }
        response = table.query(**query_params)
        unit_cost=response['Items'][0]['unit_cost']
        total_cost=total_cost+value*int(unit_cost)
    return total_cost



def updated_customer_credits(username, value_of_credits_to_update):
    query_params = {
    'KeyConditionExpression': Key(os.getenv("PARTITION_KEY_TABLE_USER")).eq(f'{username}')
    }
    response = table.query(**query_params)
    partition_key=response['Items'][0][os.getenv("PARTITION_KEY_TABLE_USER")]
    sort_key=response['Items'][0][os.getenv("SORT_KEY_TABLE_USER")]
    try:
            response = table.update_item(
                Key = {
                        os.getenv("PARTITION_KEY_TABLE_USER"):partition_key, 
                        os.getenv("SORT_KEY_TABLE_USER"):sort_key
                },
                UpdateExpression = f"SET {ATTRIBUTE_CREDITS_TABLE_USER} = :{ATTRIBUTE_CREDITS_TABLE_USER}",
                ExpressionAttributeValues ={
                    ":credits": value_of_credits_to_update},
                ReturnValues="UPDATED_NEW")
    except Exception as e:
            print(e)
    pass





def get_current_customer_credits(username):
    try:
        query_params = {
        'KeyConditionExpression': Key('username').eq(f'{username}')
        }
        response = table.query(**query_params)
        tota_credits_of_client=response['Items'][0][ATTRIBUTE_CREDITS_TABLE_USER]
        return tota_credits_of_client

    except Exception as e:
        print(e)
        return os.getenv("DECODIFICATION_TOKEN_ERROR")
    




def count_execution_models(user_id):
    table = dynamodb.Table(os.getenv("TRACKING_MODEL"))
    query_params = {
        'KeyConditionExpression': Key('user_id').eq(f'{user_id}')
    }
    response = table.query(**query_params)
    list_model_names=[]
    try:
        for item in response['Items']:
            list_model_names.append(item['model_name'])
        row_count_table_tracking_model = response['Count']
        frequency_table_usage_models = {}
        for model_name in list_model_names:
            if model_name in frequency_table_usage_models:
                frequency_table_usage_models[model_name] += 1
            else:
                frequency_table_usage_models[model_name] = 1

        name_of_component_models = list(frequency_table_usage_models.keys())
        frecuency_usage_models = list(frequency_table_usage_models.values())
    except Exception as e:
        print(f'{e}')
    build_dict_to_return = {}
    for name_of_component_model, value_frecuency_usage_model in zip(name_of_component_models, frecuency_usage_models):
        try:
            query_params = {
                    'KeyConditionExpression': Key('model_id').eq(name_of_component_model)
                }
            response = tableModelConfig.query(**query_params)
            build_dict_to_return[response['Items'][0]['title']] = value_frecuency_usage_model
        except Exception as e:
            print(f'{name_of_component_model}{value_frecuency_usage_model}{e}')
    return row_count_table_tracking_model,build_dict_to_return
    
    




def get_cost_of_usage_model(model_id):
    table = dynamodb.Table(os.getenv("MODEL_CONFIG"))
    query_params = {
            'KeyConditionExpression': Key('model_id').eq(f'{model_id}')
        }
    response = table.query(**query_params)
    return response['Items'][0]['unit_cost']





def charge_credits_to_client(user,number_of_credits_to_charge:int):
    current_customer_credits=get_current_customer_credits(user)
    credits_to_update=current_customer_credits+number_of_credits_to_charge
    query_params = {
    'KeyConditionExpression': Key(os.getenv("PARTITION_KEY_TABLE_USER")).eq(f'{user}')
    }
    response = table.query(**query_params)
    if(len(response['Items'])!=0):
        partition_key=response['Items'][0][os.getenv("PARTITION_KEY_TABLE_USER")]
        sort_key=response['Items'][0][os.getenv("SORT_KEY_TABLE_USER")]
        try:
                response = table.update_item(
                    Key = {
                            os.getenv("PARTITION_KEY_TABLE_USER"):partition_key, 
                            os.getenv("SORT_KEY_TABLE_USER"):sort_key
                    },
                    UpdateExpression = f"SET {ATTRIBUTE_CREDITS_TABLE_USER} = :{ATTRIBUTE_CREDITS_TABLE_USER}",
                    ExpressionAttributeValues ={
                        ":credits": credits_to_update},
                    ReturnValues="UPDATED_NEW")
                return number_of_credits_to_charge
        except Exception as e:
                print(e)
    else:
        return os.getenv("DECODIFICATION_TOKEN_ERROR")






def send_email_with_verification_code(recipient, code):
    SENDER = os.getenv("SENDER_EMAIL")
    RECIPIENT = recipient
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = 587
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    
    styles = """
    <style>
        body {
            font-family: Arial, sans-serif;
            font-size: 14px;
        }
        h2 {
            color: #9b9b9b;
        }
        .button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
            transition: all 0.3s ease-in-out;
        }

        .button:hover {
            background-color: #3e8e41;
            transform: translateY(-1px);
        }

        .logo {
            width: 50px;
            margin-bottom: 20px;
        }
    </style>
    """
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = RECIPIENT
    msg['Subject'] = "Code verification CAOBA"

    print(os.getcwd())

    with open('images/caoba-alianza-privada-big-data.png', 'rb') as f:
        logo = MIMEImage(f.read())
        logo.add_header('Content-ID', '<logo>')
        msg.attach(logo)

    body = f"""
        {styles}
        <h3>Verify your email address</h3>
        <h3>Please click the following link to verify your email:</h3>
        <h3><a href="https://backend-api-app.caobalab.co/user/verify/{code}" class="button">Verify email</a></h3>
        <img src="cid:logo" class="logo">

    """
    msg.attach(MIMEText(body, 'html'))
    smtp_client = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp_client.ehlo()
    smtp_client.starttls()
    smtp_client.ehlo()
    smtp_client.login(SMTP_USERNAME, SMTP_PASSWORD)
    smtp_client.sendmail(SENDER, RECIPIENT, msg.as_string())
    smtp_client






def change_status_verification_code(username):
    query_params = {
    'KeyConditionExpression': Key(os.getenv("PARTITION_KEY_TABLE_USER")).eq(f'{username}')
    }
    response = table.query(**query_params)
    partition_key=response['Items'][0][os.getenv("PARTITION_KEY_TABLE_USER")]
    sort_key=response['Items'][0][os.getenv("SORT_KEY_TABLE_USER")]
    try:
            response = table.update_item(
                Key = {
                        os.getenv("PARTITION_KEY_TABLE_USER"):partition_key, 
                        os.getenv("SORT_KEY_TABLE_USER"):sort_key
                },
                UpdateExpression = f"SET {ATTRIBUTE_IS_VERIFIED_TABLE_USERS} = :{ATTRIBUTE_IS_VERIFIED_TABLE_USERS}",
                ExpressionAttributeValues ={
                    ":is_verified": True},
                ReturnValues="UPDATED_NEW")
    except Exception as e:
            print(e)





def generate_token(username: str):
    access_token_expires = datetime.utcnow() + timedelta(minutes=5)
    access_token = jwt.encode({"sub": username, "exp": access_token_expires}, JWT_SECRET_TOKEN_EMAIL, algorithm=JWT_ALGORITHM_TOKEN_EMAIL)
    return access_token





def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET_TOKEN_EMAIL, algorithms=[JWT_ALGORITHM_TOKEN_EMAIL])
        email = payload.get("sub")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid verification code")
    



    
def get_email_by_username(username):
    try:
        query_params = {
        'KeyConditionExpression': Key('username').eq(f'{username}')
        }
        response = table.query(**query_params)
        return response['Items'][0][ATTRIBUTE_EMAIL_TABLE_USER]

    except Exception as e:
        print(e)
        return os.getenv("DECODIFICATION_TOKEN_ERROR")
    


    
def get_verify_email_status(username):
    try:
        query_params = {
        'KeyConditionExpression': Key('username').eq(f'{username}')
        }
        response = table.query(**query_params)
        if(response['Items'][0][ATTRIBUTE_IS_VERIFIED_TABLE_USERS])==False:
            print("No Verificado")
            verification_code_jwt=generate_token(username)
            email=get_email_by_username(username)
            print("email query......",email)
            send_email_with_verification_code(email,verification_code_jwt)
            return "EMAIL SENT"
        else:
            return "USER VERIFIED"
    except Exception as e:
        print(e)
        return os.getenv("DECODIFICATION_TOKEN_ERROR")
    

from io import BytesIO

def get_report_usage(init_date:str,final_date:str):
    try:
        client_dynamo=load_dynamoclient()
        table_name = 'aaas_tracking_models'

        filter_expression = "#attribute1 > :value1 AND #attribute1 < :value2 "
        expression_attribute_values = {
            ":value1": {'S': init_date},
            ":value2": {'S': final_date},
        }
        expression_attribute_names = {
            "#attribute1": 'created_at'
        }
        response = client_dynamo.scan(
            TableName=table_name,
            FilterExpression=filter_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names
        )
        cast_response_to_dataframe = pd.DataFrame(response['Items']) 
        return cast_response_to_dataframe
    
    except Exception as e:
        print(e)
        return os.getenv("DECODIFICATION_TOKEN_ERROR")