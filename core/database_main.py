from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy import or_, not_, func, text, ForeignKey, DateTime, Table, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import datetime

SQLAlCHEMY_DATABASE_URL = "sqlite:///./sqlite_main.db"

engine = create_engine (SQLAlCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

class Person(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, autoincrement = True)
    username = Column(String())

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()