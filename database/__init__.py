import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config.db import DB_URL_INTERNAL



engine = create_engine(DB_URL_INTERNAL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 

def get_db():
    '''used to create session for endpoints to make queries to DB'''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class CreateTableError(Exception):
    pass

def create_tables(try_times, wait_seconds):
    '''
    This function gets called when the FastAPI service starts.
    It will create tables defined in database/models.py if not created yet.
    Because the service might try to create tables before the DB is ready (which will cause error),
    while loop is implemented to ensure the service will try some times before giving up.
    '''
    count = 0
    success = False
    while count < try_times:
        try:
            Base.metadata.create_all(bind=engine)
            success = True
            break
        except:
            pass
        count += 1
        time.sleep(wait_seconds)
    if not success:
        raise CreateTableError('Failed to create tables in MySql container.')




        
