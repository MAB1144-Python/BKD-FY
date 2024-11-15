from sqlalchemy.orm import Session
from schemas.schemas_user import User, UserCreate
from passlib.context import CryptContext
import psycopg2
from utils.config import load_config
import os
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, document: str):
    return query_user_exists(document)

def create_user(user: User):
    """ Insert a new user into the users_ferroelectricos_yambitara table """
    sql = f"""INSERT INTO {os.getenv('DB_USER_TABLE')} (username, hashed_password, email, document, name, type_document, contact_user, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
    hashed_password = pwd_context.hash(user.password)
    print(user)
    data = (user.user_id, hashed_password, user.email, user.document, user.name, user.type_document, user.contact_user, user.created_at)
    user_id = query_db_insert(sql, data)
    print("user_id",user_id)
    return user_id

def query_user_exists(document: str) -> bool:
    sql = f"SELECT 1 FROM {os.getenv('DB_USER_TABLE')} WHERE document = %s"
    exists = False
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (document,))
                exists = cur.fetchone() is not None
    except (Exception, psycopg2.DatabaseError) as error:
        print("presento el error ",error)
    return {"message":exists}


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

def query_db_insert(sql_query, data):
    try:
        config = load_config()
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql_query, (data,))
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return{"message":"Creado con exito"}


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
