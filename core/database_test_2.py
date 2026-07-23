from sqlalchemy import create_engine, Column, Integer, String, Boolean, or_, not_, func, text,ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

SQLAlCHEMY_DATABASE_URL = "sqlite:///./sqlite_2.db"

engine = create_engine (SQLAlCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

session = SessionLocal()

Base = declarative_base()

class User (Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, autoincrement = True)
    username = Column(String)
    email = Column(String, unique = True, index = True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default = True)

    addressess = relationship("Address")
    profile = relationship("Profile", backref = "user", uselist = False)

    def __repr__(self):
        return f"User (id = {self.id!r}, email = {self.email
                                                  !r}, username = {self.username!r})"
    

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    city = Column(String())
    state = Column(String())
    zip_code = Column(String())
    
    def __repr__(self):
        return f"id ={self.id}, user_id={self.user_id}, city={self.city}"
        
class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey("users.id"), unique = True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer, nullable = True)
    bio = Column(String, nullable = True)

    def __repr__(self):
            return f"id ={self.id}, First_name={self.first_name}, last_name={self.last_name}"


Base.metadata.create_all(engine)

'''Maryam = User(username = "Maryam Love" ,email = "Maryam@yahoo.com",  hashed_password = "255df")
Anita = User(username = "Anita Pasha" ,email = "Anita@yahoo.com",  hashed_password = "2jtgdf")
Mehdi = User(username = "MehdiOstad" ,email = "Mehdi@yahoo.com",  hashed_password = "1248dfsdf")
Users = [Maryam, Anita, Mehdi]
session.add_all(Users)
session.commit()'''

'''user = session.query(User).filter(or_(User.email == "Mehdi@yahoo.com",
                                       User.hashed_password == "20")).first()
addresses = [Address(user_id = user.id, city = "Tehran", state = "Tehran",
                      zip_code = "12346"), Address(user_id = user.id, city = "Abad", 
                                                   state = "Semnan", zip_code = "1258")]

session.add_all(addresses)
session.commit()'''

'''session.add(Profile(user_id = user.id, first_name = "Mehdi", last_name = "Ostad"))
session.commit()'''

Total_users = session.query(func.count(Profile.id)).scalar()
print("Total users:", Total_users)

user = session.query(User).filter(or_(User.email == "Mehdi@yahoo.com",
                                       User.hashed_password == "20")).first()
print(user.profile.last_name)

profile_1 = session.query(Profile).filter_by(first_name = "Mehdi").first()
print(profile_1)

print(profile_1.user.username)

session.close()