from sqlalchemy.orm import Session
from fastapi import APIRouter,FastAPI, Depends, HTTPException, status
from schemas.schemas_user import User, UserCreate
from passlib.context import CryptContext
import psycopg2
from utils.config import load_config
import os
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_all_users():
    sql = f"SELECT * FROM {os.getenv('DB_USER_TABLE')}"
    users = []
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                users = cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: ", error)
    return users



def query_db_delete(sql_query, data):
    try:
        config = load_config()
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql_query, (data,))
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return{"message":False}
    return{"message":True}
