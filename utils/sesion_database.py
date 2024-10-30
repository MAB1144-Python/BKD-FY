from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2 import sql
import time
import random
from sqlalchemy import create_engine


db_name = 'postgres'
db_user = 'user'
db_pass = 'Mab880821'
db_host = '127.0.0.1'
db_port = '5432'

# def create_database():
#     conn = psycopg2.connect(
#         dbname="postgres",
#         user="user",
#         password="Mab880821",
#         host="localhost",
#         port="5432"
#     )
#     conn.autocommit = True
#     cursor = conn.cursor()

#     cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'usuarios'")
#     exists = cursor.fetchone()
#     if not exists:
#         cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier('usuarios')))
#         print("Database created successfully")
#     else:
#         print("Database already exists")

#     cursor.close()
#     conn.close()

# create_database()


# # Connect to the database
# engine = create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')

# while True:
#     print("Checking connection")
#     with engine.connect() as connection:
#         result = connection.execute("SELECT 1")
#         print(result.fetchone())
#     time.sleep(5)




# Replace 'DATABASE_URL' with your actual database URL
DATABASE_URL = "postgresql://user:Mab880821@localhost:5432/usuarios"
#DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    return db



