from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

class Post(Base):
    __tablename__ = "posts_sqlalchemy"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_on = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))
    owner = Column(String, ForeignKey("users.username", ondelete="CASCADE"), nullable=False)
    
class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_on = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))
    
class Like(Base):
    __tablename__ = "like"
    username = Column(String, ForeignKey("users.username", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts_sqlalchemy.id", ondelete="CASCADE"), primary_key=True)
    
