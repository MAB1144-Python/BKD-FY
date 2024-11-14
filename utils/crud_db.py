from utils.crud import get_user_by_username, create_user, query_db_insert
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from utils.config import load_config
import psycopg2

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def query_user_exists_email(email: str):
    sql = f"SELECT * FROM {os.getenv('DB_USER_TABLE')} WHERE email = %s"
    exists = False
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (email,))
                exists = cur.fetchone() is not None
            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("presento el error ",error)
    return {"message":exists}

def query_user_exists(document: str):
    sql = f"SELECT * FROM {os.getenv('DB_USER_TABLE')} WHERE document = %s"
    exists = False
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (document,))
                exists = cur.fetchone() is not None
            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("presento el error ",error)
    return {"message":exists}


def query_db_insert(sql_query, data):
    vendor_id = None
    try:
        config = load_config()
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql_query, data)
                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("error ",error)
    finally:
        return vendor_id
    

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