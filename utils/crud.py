from sqlalchemy.orm import Session
from schemas.schemas_user import User, UserCreate
from passlib.context import CryptContext
import psycopg2
from utils.config import load_config
import os
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, document: str):
    return query_user_exists(document)


# def create_user(user: UserCreate):
#     print(""" Insert a new vendor into the vendors table """)
#     sql = """INSERT INTO vendors(vendor_name)
#              VALUES(%s) RETURNING vendor_id;"""
#     vendor_id = None
#     sql = """INSERT INTO users_ferroelectricos_yambitara (username, hashed_password, email)
#              VALUES (%s, %s, %s) RETURNING id;"""
#     hashed_password = pwd_context.hash(user.password)
#     data = (user.username, hashed_password, user.email)
#     user_id = query_db_insert(sql, data)
#     return user_id

# def create_user(user: User):
#     print("linea 30",user)
#     """ Insert a new user into the users_ferroelectricos_yambitara table """
#     sql = """INSERT INTO users_ferroelectricos_yambitara (user_id, password, email, document, name, type_document, contact_user)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s);"""
#     hashed_password = pwd_context.hash(user.password)
#     print("linea 30",user)
#     data = (user.user_id, hashed_password, user.email, user.document, user.name, user.type_document, user.contact_user)
#     data = ("hola", "hola", "hola", "hola", "hola", "hola", "hola")
#     user_id = query_db_insert(sql, data)
#     return user_id
    
    
# def query_db_insert(sql_query, data):
#     vendor_id = None
#     try:
#         config = load_config()
#         with  psycopg2.connect(**config) as conn:
#             with  conn.cursor() as cur:
#                 # execute the INSERT statement
#                 print("data",data)
#                 cur.execute(sql_query, data)
#                 # get the generated id back
#                 rows = cur.fetchone()
#                 if rows:
#                     vendor_id = rows[0]
#                 # commit the changes to the database
#                 conn.commit()
#         print("get ",get_all_users())
#     except (Exception, psycopg2.DatabaseError) as error:
#         print("error error",error)
#     finally:
#         return vendor_id


# def query_user_exists(document: str):
#     sql = "SELECT * FROM users_ferroelectricos_yambitara WHERE document = %s"
#     exists = False
#     try:
#         print("get 64")
#         config = load_config()
#         print("get 66")
#         with psycopg2.connect(**config) as conn:
#             with conn.cursor() as cur:
#                 print("get 67")
#                 cur.execute(sql, (document,))
#                 print("get 68")
#                 exists = cur.fetchone() is not None
#             # commit the changes to the database
#             conn.commit()
#         print("get ")
#     except (Exception, psycopg2.DatabaseError) as error:
#         print("presento el error ",error)
#     return {"message":exists}


# def query_user_exists(document: str) -> bool:
#     sql = "SELECT 1 FROM users_ferroelectricos_yambitara WHERE document = %s"
#     exists = False
#     try:
#         config = load_config()
#         with psycopg2.connect(**config) as conn:
#             with conn.cursor() as cur:
#                 cur.execute(sql, (document,))
#                 exists = cur.fetchone() is not None
#     except (Exception, psycopg2.DatabaseError) as error:
#         print("presento el error ",error)
#     return {"message":exists}

# def get_all_users():
#     sql = "SELECT * FROM users_ferroelectricos_yambitara"
#     users = []
#     try:
#         config = load_config()
#         with psycopg2.connect(**config) as conn:
#             with conn.cursor() as cur:
#                 cur.execute(sql)
#                 users = cur.fetchall()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print("Error: ", error)
#     return users


    