from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

db_username = os.getenv("DB_USERNAME", "postgres")
db_password = os.getenv("DB_PASSWORD", "postgres")

DATABASE_URL = f"postgresql://{db_username}:{db_password}@db:5432/finance_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()