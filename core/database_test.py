from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

SQLAlCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"

engine = create_engine (SQLAlCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

class User (Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, autoincrement = True)
    first_name = Column(String)
    last_name = Column(String)
    title = Column(String, nullable = True)
    email = Column(String, unique = True, index = True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default = True)

    @property
    def get_fullname(self):
        return self.first_name+" "+self.last_name

    def __repr__(self):
        return f"User (id = {self.id!r}, email = {self.email!r}, full_name = {self.get_fullname!r})"
        

Base.metadata.create_all(engine)

