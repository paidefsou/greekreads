from fastapi import Body, FastAPI, HTTPException, Response, status, Depends, APIRouter
from typing import  List, Optional

from sqlalchemy import func

from .. import models, schemas, oauth2
from ..database import get_db

from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/books",
    tags= ["Books"]
)


@router.get("/", response_model=List[schemas.BookOut])
def get_books(db: Session = Depends(get_db), 
              current_user:int = Depends(oauth2.get_current_user),
             limit: int=5, skip: int=3, search: Optional[str] = ""):
    # # with raw sql
    # cursor.execute("""SELECT * FROM books""")
    # books = cursor.fetchall()
    
    
  
    # this way you have only the current users books
    # books = db.query(models.Book).filter(models.Book.owner_id==current_user.id).all()
    
    books = db.query(models.Book, func.count(models.Vote.book_id).label("votes")).join(
        models.Vote, models.Vote.book_id==models.Book.id,
        isouter=True).group_by(models.Book.id).filter(models.Book.title.contains(search  )).limit(limit).offset(skip).all()
    
    # return {"data":books}
    return books # instead of the above we just return books and fastapi will automatically serialize it and convert it to json 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Book)
def create_books(book: schemas.BookCreate, db: Session = Depends(get_db), current_user :int = Depends(oauth2.get_current_user)):    
    # cursor.execute(""" INSERT INTO books(title, author, description, read, rating) VALUES (%s, %s, %s, %s, %s) RETURNING *""", (book.title,
    #                book.author, book.description, book.read, book.rating))
    # new_book = cursor.fetchone()
    # conn.commit()
    
    # new_book = models.Book(title=book.title, author=book.author, description=book.description, read=book.read, rating=book.read)
    print(current_user.id)
    new_book = models.Book(owner_id=current_user.id, **book.dict()) # instead of the above line you can unpack the dict with **
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book



@router.get("/{id}", response_model=schemas.BookOut)
def get_book(id:int, db: Session = Depends(get_db), 
             current_user :int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM books WHERE id= %s """, (str(id),)) #using %s and a second parameter in order to avoid sql injection
    # book = cursor.fetchone()
    
    book = db.query(models.Book, func.count(models.Vote.book_id).label("votes")).join(
        models.Vote, models.Vote.book_id==models.Book.id,
        isouter=True).group_by(models.Book.id).filter(models.Book.id == id).first()  # if i put all it would be a waste of resources
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    # if i want to let only current user retrieve his books i can implement the functionality alreaedy exists in delete and put
    
    return book


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id:int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""DELETE FROM books WHERE id= %s RETURNING * """, (str(id),)) #using %s and a second parameter in order to avoid sql injection
    # deleted_book = cursor.fetchone()
    # conn.commit()
    
    book_query = db.query(models.Book).filter(models.Book.id == id)
    
    book = book_query.first()
    if book == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"book with id: {id} was not found")
    
    if book.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    book_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Book)
def update_book(id:int, updated_book : schemas.BookCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE books SET title= %s, author= %s, description= %s, read= %s, rating= %s WHERE id=%s RETURNING *""",(book.title,
    #                book.author, book.description, book.read, book.rating, str(id)))
    # updated_book = cursor.fetchone()
    # conn.commit()
    
    book_query = db.query(models.Book).filter(models.Book.id == id)
    book = book_query.first()
    
    if book== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"book with id: {id} was not found")
    
    if book.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    book_query.update(updated_book.dict(), synchronize_session=False) # the dict refers to the pydantic model 
                                                                      # which is asigned in the declaration above i cannot dict an orm model which is the book in this line explanation 5h 28 min in video
    db.commit()
    
    return book_query.first()
