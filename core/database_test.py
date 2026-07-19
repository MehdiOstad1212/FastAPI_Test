from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

SQLAlCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"

engine = create_engine (SQLAlCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

session = SessionLocal()

Base = declarative_base()

class User (Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, autoincrement = True)
    first_name = Column(String)
    last_name = Column(String, nullable = True)
    age = Column(Integer)
    title = Column(String, nullable = True)
    email = Column(String, unique = True, index = True)
    hashed_password = Column(String, nullable = True)
    is_active = Column(Boolean, default = True)

    '''@property
    def get_fullname(self):
        return self.first_name+" "+self.last_name'''

    def __repr__(self):
        return f"User (id = {self.id!r}, email = {self.email!r}, first_name = {self.first_name!r})"
        

Base.metadata.create_all(engine)

# Inserting Data
Mehdi = User(first_name = "Mehdi",  age = 27)
session.add(Mehdi)
session.commit()

#Bulk Inserting 
'''Maryam = User(first_name = "Meryam",  age = 25)
Anita = User(first_name = "Anita",  age = 14)
Users = [Maryam, Anita]
session.add_all(Users)
session.commit()'''

#Retrieve Data
users = session.query(User).all()
print (users)

#Retrieve A Part Of Data
user = session.query(User).filter_by(first_name = "Mehdi").first()
print (user)

#Updating An item of Data
user.last_name = "Ostad"
session.commit()

#Deleting An item of Data
'''if user:
    session.delete(user)
    session.commit()'''

