from sqlalchemy import create_engine, Column, Integer, String, Boolean, or_, not_, func, text,ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

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

    addressess = relationship("Address")


    '''@property
    def get_fullname(self):
        return self.first_name+" "+self.last_name'''

    def __repr__(self):
        return f"User (id = {self.id!r}, email = {self.email
                                                  !r}, first_name = {self.first_name!r})"
    

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    city = Column(String())
    state = Column(String())
    zip_code = Column(String())
    
    def __repr__(self):
        return f"id ={self.id}, user_id={self.user_id}, city={self.city}"
        

Base.metadata.create_all(engine)

# Inserting Data
'''Mehdi = User(first_name = "Mehdi",  age = 27)
session.add(Mehdi)
session.commit()'''

#Bulk Inserting 
'''Maryam = User(first_name = "Meryam",  age = 25)
Anita = User(first_name = "Anita",  age = 14)
Users = [Maryam, Anita]
session.add_all(Users)
session.commit()'''

#Retrieve Data
'''users = session.query(User).all()
print (users)'''

#Retrieve A Part Of Data
'''user_s = session.query(User).filter_by(first_name = "Meryam").first()
print (user_s)

#Updating An item of Data
user_s.last_name = "Naza"
user_s.first_name = "Maryam"
session.commit()'''

'''user = session.query(User).filter(User.age > 20).all()
print (user)'''

#Deleting An item of Data
'''if user:
    session.delete(user)
    session.commit()'''

user = session.query(User).filter(or_(User.first_name == "Mehdi", User.age > 20)).first()
print (user)
A = user.addressess

'''addresses = [Address(user_id = user.id, city = "Tehran", state = "Tehran",
                      zip_code = "12346"), Address(user_id = user.id, city = "Abad", 
                                                   state = "Semnan", zip_code = "1258")]

session.add_all(addresses)
session.commit()'''

Addresses_1 = session.query(Address).filter_by(user_id = user.id, city = "Tehran").all()
print(Addresses_1)

user = session.query(User).filter(User.first_name.like("me%")).all()
print (user)

Total_users = session.query(func.count(User.id)).scalar()
print("Total users:", Total_users)

Average_age = session.query(func.avg(User.age)).scalar()
print("Age average:", Average_age)

max_age = session.query(func.max(User.age)).scalar()
min_age = session.query(func.min(User.age)).scalar()
print(f"Maximum age is: {max_age}, Minimum age is : {min_age}")

Total_users_age = session.query(func.sum(User.age)).scalar()
print("Total age of users is:", Total_users_age)

query = text("SELECT AVG(age) FROM users")
result = session.execute(query).scalar()
print("Age average:", result)

query = text("SELECT * FROM users WHERE first_name= :name")
result = session.execute(query,{"name":"Mehdi"}).fetchall()
print("Users named Mehdi:", [user.first_name for user in result])

session.close()