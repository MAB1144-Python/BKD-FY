from sqlalchemy.orm import Session
from schemas.shemas_user import User, UserCreate
from passlib.context import CryptContext
import psycopg2
from utils.config import load_config
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, document: str):
    return db.query(UserCreate).filter(UserCreate.document == document).first()


def create_user(user: UserCreate):
    """ Insert a new vendor into the vendors table """
    sql = """INSERT INTO vendors(vendor_name)
             VALUES(%s) RETURNING vendor_id;"""
    vendor_id = None
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (vendor_name,))
                # get the generated id back
                rows = cur.fetchone()
                if rows:
                    vendor_id = rows[0]
                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return vendor_id

    