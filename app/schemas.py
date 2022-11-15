from turtle import st
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint



# class Book(BaseModel):    
#     title: str
#     author: str
#     description: str
#     read: bool = False
#     rating: Optional[int] = None  
    
class BookBase(BaseModel):    
    title: str
    author: str
    description: str
    read: bool = False
    rating: Optional[int] = None
    
    
class BookCreate(BookBase):
    pass
   
class UserOut(BaseModel):  # Response
    id:int
    email : EmailStr
    created_at: datetime
    
    class Config:  # so it is recognised by sqlalchemy 
        orm_mode = True

class Book(BookBase): #response model
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:  # so it is recognised by sqlalchemy 
        orm_mode = True
        

class BookOut(BaseModel):
    Book: Book
    votes: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str
    
   
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token:  str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str]
    
class Vote(BaseModel):
    book_id: int
    dir: conint(le=1) # less or equal to one ..