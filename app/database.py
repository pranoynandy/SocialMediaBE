from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings
import time

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()



'''
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='SocialMedia', user='postgres',password='password',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection Successful")
        break

    except Exception as error:
        print("Connection Failed")
        print("Error =", error)
        time.sleep(2)

cursor.execute("""
CREATE TABLE IF NOT EXISTS post_psycopg2 (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50),
    content VARCHAR(300));""")
conn.commit()
'''