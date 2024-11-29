from fastapi import APIRouter,FastAPI, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from utils.config import load_config
import psycopg2
import os
import pandas as pd

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def query_user_exists_email(email: str):
    sql = f"SELECT * FROM {os.getenv('DB_USER_TABLE')} WHERE email = %s"
    print("sql ",sql,email)
    exists = False
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (email,))
                result = cur.fetchall()
                df = pd.DataFrame(result, columns=[desc[0] for desc in cur.description])
                print("df ",df)
                exists = not df.empty
            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("presento el error ",error)
        raise HTTPException(status_code=400, detail="Error in the server")
    return {"message":exists}

def query_user_exists_document(document: str):
    sql = f"SELECT * FROM {os.getenv('DB_USER_TABLE')} WHERE document = %s"
    exists = False
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (document,))
                result = cur.fetchall()
                df = pd.DataFrame(result, columns=[desc[0] for desc in cur.description])
                exists = not df.empty
            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("presento el error ", error)
        raise HTTPException(status_code=400, detail="Error in the server")
    return {"message": exists}

def query_product_exists(product_id: str):
    sql = f"SELECT product_name FROM {os.getenv('DB_PRODUCT_TABLE')} WHERE product_id = %s"
    product_name = None
    exists = False
    print("product_id ",product_id)
    print("sql ",sql) 
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (product_id,))
                result = cur.fetchall()
                df = pd.DataFrame(result, columns=[desc[0] for desc in cur.description])
                exists = not df.empty
                result = cur.fetchone()
                if result:
                    product_name = result[0]
            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("presento el error ", error)
    return {"message":exists,"product_name": product_name}

def query_user_exists_supplier(supplier_nit: str):
    sql = f"SELECT * FROM {os.getenv('DB_SUPPLIER_TABLE')} WHERE supplier_nit = %s"
    exists = False
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (supplier_nit,))
                result = cur.fetchall()
                df = pd.DataFrame(result, columns=[desc[0] for desc in cur.description])
                exists = not df.empty
            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("presento el error ",error)
    return {"message":exists}

def query_user_exists_products(product_name: str):
    sql = f"SELECT * FROM {os.getenv('DB_PRODUCT_TABLE')} WHERE product_name = %s"
    exists = False
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (product_name,))
                result = cur.fetchall()
                df = pd.DataFrame(result, columns=[desc[0] for desc in cur.description])
                exists = not df.empty
            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("presento el error ",error)
    return {"message":exists}

def query_user_exists_products_id(product_id: str):
    sql = f"SELECT * FROM {os.getenv('DB_PRODUCT_TABLE')} WHERE product_id = %s"
    exists = False
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (product_id,))
                result = cur.fetchall()
                print("result ",result)
                df = pd.DataFrame(result, columns=[desc[0] for desc in cur.description])
                print("df ",df)
                exists = df.empty
                print("exists ",exists)
            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("presento el error ",error)
    return {"message":exists}

def query_db_insert(sql_query, data):
    try:
        config = load_config()
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql_query, data,)
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("error db",error)
        raise HTTPException(status_code=400, detail="Error in the server")
    return{"message":"Creado con exito"}

def query_db_fetchone(sql_query: str, data: tuple):
    try:
        config = load_config()
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql_query, data,)
                result = cur.fetchone()
                print("result ",result)
                conn.commit()
                return {"message":result}
    except (Exception, psycopg2.DatabaseError) as error:
        print("error db",error)
        raise HTTPException(status_code=400, detail="Error in the server")

def query_db_fetchall(query: str):
    try:
        config = load_config()
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur: 
                # execute the INSERT statement
                cur.execute(query)
                result = cur.fetchall()
                print("result ",result)
                conn.commit()
                return {"message":result}
    except (Exception, psycopg2.DatabaseError) as error:
        print("error db",error)
        raise HTTPException(status_code=400, detail="Error in the server")

  
def query_db_update(sql_query, data):
    print("sql_query ",sql_query)
    print("data ",data)
    try:
        config = load_config()
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql_query, data,)
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("uptade product: ",error)
        raise HTTPException(status_code=400, detail="Update failed")
    return{"message":"Update success"}

def get_all_users():
    sql = "SELECT * FROM users_ferroelectricos_yambitara"
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

def query_db(query: str):
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
                print(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    