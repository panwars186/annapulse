
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from app.core.config import DATABASE_URL

#load_dotenv()

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base = declarative_base()