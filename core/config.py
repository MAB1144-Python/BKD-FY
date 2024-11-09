import os
from dotenv import load_dotenv
# from pydantic import  BaseSettings

load_dotenv()

class Settings():#BaseSettings):

    JWT_SECRET_KEY: str='JWT_SECRET_KEY'
    JWT_REFRESH_SECRET_KEY: str='JWT_REFRESH_SECRET_KEY'   
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    JWT_SECRET_KEY_ADMIN: str='JWT_SECRET_KEY_ADMIN'

settings = Settings()
