from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import database


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:syspass@localhost/fastapi'
# SQLALCHEMY_DATABASE_URL = 'postgresql://nattkarn:og7Ddpi6ZckR@ep-broken-credit-91944191.ap-southeast-1.aws.neon.tech/backend?sslmode=require'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()