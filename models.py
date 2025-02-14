from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id=Column(String, primary_key=True,index=True)
    login=Column(String,unique=True,index=True)
    avatar_url=Column(String)

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer, index=True)
    owner = Column(String)
    repo = Column(String)
    created_at = Column(DateTime(timezone=True),server_default=func.now())