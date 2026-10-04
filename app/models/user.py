from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import  Column, Integer, String, ForeignKey

class Base(DeclarativeBase): pass 

class Users(Base):
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key = True, index=True)
    email = Column(String)
    password = Column(String)
    name = Column(String)
    
class Tasks(Base):
    __tablename__ = "Tasks"
    
    id = Column(Integer, primary_key = True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    user_task_number = Column(Integer)
    title = Column(String)
    description = Column(String)
    tag_id = Column(Integer, ForeignKey("Tags.id"))
    
    tag = relationship("Tags")
        
class Tags(Base):
    __tablename__ = "Tags"
    
    id = Column(Integer, primary_key = True)
    name = Column(String)

