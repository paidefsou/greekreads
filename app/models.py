from typing import Optional
from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(String, nullable=False)
    read = Column(Boolean, nullable=False, server_default='FALSE') #Jjust default will not work with the ORM we need server_default
    rating = Column(Integer, nullable=False)
    created_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User")

    
class User(Base):
    __tablename__  ="users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique = True)
    password = Column(String, nullable=False)
    created_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
  
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    book_id = Column(Integer, ForeignKey(
        "books.id", ondelete="CASCADE"), primary_key=True)