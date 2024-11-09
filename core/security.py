from passlib.context import CryptContext
from typing import Union, Any
from datetime import datetime, timedelta
from jose import jwt
from core.config import settings

password_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")



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



def create_refresh_token(subject:Union[str, Any], expires_delta: int = None) -> str:
    """
    description: Function to create a JWT token with username, the token will expire after 2.8 hours
    input: a username 
    output: a string with the token created with JWT token
    """
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes = 10080 )
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    enconded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, algorithm='HS256')
    return enconded_jwt

    

def get_password(password: str) -> str:
    """
    description: Function to create the hash of the password
    input: a password as a string
    output: a string with the hash of the password
    """
    return password_context.hash(password)



def verify_password(password: str, hashed_pass: str) -> bool:
    """
    description: Function to validate hash of the password
    input: a password and hashed_password as a string
    output: a boolean indicating if the password make match or not: false is not verified
    """
    print("security 59", password)
    print("security 59", hashed_pass)
    print("security 59",password_context.verify(password, hashed_pass))
    return password_context.verify(password, hashed_pass)



def validate_token(token: str) -> dict:
    """
    description: Function to validate the token generated in the login, It is used to unblock route.
    input: a token as a string.
    output: a dict or JSON with information of the user otherwise a empty dict or empty JSON.
    example of output: {'exp': 1696729776, 'sub': 'usertest1'}
    """
    try:
        payload_decode: dict = jwt.decode(token, key=settings.JWT_SECRET_KEY, algorithms=['HS256'])
    except:
        payload_decode={}
    return payload_decode



def create_acess_token_admin(subject:Union[str, Any], expires_delta: int = None) -> str:
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
    enconded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY_ADMIN, algorithm='HS256')
    return enconded_jwt


def validate_token_admin(token: str) -> dict:
    """
    description: Function to validate the token generated in the login, It is used to unblock route.
    input: a token as a string.
    output: a dict or JSON with information of the user otherwise a empty dict or empty JSON.
    example of output: {'exp': 1696729776, 'sub': 'usertest1'}
    """
    try:
        payload_decode: dict = jwt.decode(token, key=settings.JWT_SECRET_KEY_ADMIN, algorithms=['HS256'])
        print(payload_decode)
    except:
        payload_decode={}
        print(f"error: with,{payload_decode}")
    return payload_decode
