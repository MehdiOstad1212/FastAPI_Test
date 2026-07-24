from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy import or_, not_, func, text, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import datetime

SQLAlCHEMY_DATABASE_URL = "sqlite:///./sqlite_3.db"

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

    post = relationship("Post", backref = "user")

    def __repr__(self):
        return f"User (id = {self.id!r}, email = {self.email
                                                  !r}, username = {self.username!r})"
    
class Post (Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String())
    content = Column(Text())
    created_date = Column(DateTime(), default = datetime.datetime.now())
    updated_date = Column(DateTime(), default = func.now(), onupdate = func.now())

    comments = relationship("Comment", backref = "post")

    def __repr__(self):
        return f"Post(id = {self.id}, title = {self.title})"

    
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable = True)
    content = Column(Text())
    created_date = Column(DateTime(), default = func.now())

    parent = relationship("Comment", back_populates = "children", remote_side = [id])
    children = relationship("Comment", back_populates = "parent", remote_side = [parent_id])

    def __repr__(self):
        return f"Comment (id = {self.id}, user_id = {self.user_id}, post_id = {self.post_id}), parent_id = {self.parent_id}"



Base.metadata.create_all(engine)


'''Maryam = User(username = "MaryamLove" ,email = "Maryam@love.com",  hashed_password = "255df")
Anita = User(username = "AnitaPasha" ,email = "Anita@yahoo.com",  hashed_password = "2jtgdf")
Mehdi = User(username = "MehdiOstad" ,email = "Mehdi@gmail.com",  hashed_password = "1248dfsdf")
Users = [Maryam, Anita, Mehdi]
session.add_all(Users)
session.commit()'''

user = session.query(User).filter(or_(User.email == "Mehdi@gmail.com",
                                       User.hashed_password == "20")).first()
'''session.add(Post(user_id = user.id, title = "example_1", content = "post content_1"))
session.commit()

user = session.query(User).filter(or_(User.email == "Maryam@love.com",
                                       User.hashed_password == "20")).first()
session.add(Post(user_id = user.id, title = "example_2", content = "post content_2"))
session.commit()'''

post = user.post[0]

'''session.add(Comment(user_id = user.id, post_id = post.id, content = "This is a parent comment"))
session.commit()'''

post_comment = post.comments[0]

'''session.add(Comment(user_id = user.id, post_id = post.id, parent_id = post_comment.id,
                     content = "This is the first reply comment"))
session.commit()

session.add(Comment(user_id = user.id, post_id = post.id, parent_id = post_comment.id,
                     content = "This is the second reply comment"))
session.commit()'''

comments = session.query(Comment).filter_by(post_id = post.id, parent_id = None).all()

print (comments)

for comment in comments:
    print (comment.children)

user = session.query(User).filter(or_(User.email == "Maryam@love.com",
                                       User.hashed_password == "20")).first()
post = user.post[0]
print (post)
post.title = "example_2_new"
session.commit()

session.close()