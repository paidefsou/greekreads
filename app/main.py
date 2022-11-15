from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import book, user, auth, vote
from .config import Settings

# after alembic we do not need it
# models.Base.metadata.create_all(bind=engine) 

app = FastAPI()

origins = ["*"] # the domain of the app i am working on essentially

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

app.include_router(book.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


# ********before DB************
# my_books = [
#     {"title":"Three masquteers",
#      "author":"Doumas Alexander",
#      "description":"Really interesting all for one",
#      "id":1},
#     {"title":"Crime and Punishment",
#      "author":"Fyodor Dostoyefski",
#      "description":"You do it you pay it",
#      "id":2}
#     ]

# def find_book(id):
#     for b in my_books:
#         if b["id"] ==id:
#             return b
        
# def find_index_book(id):
#     for i, b in enumerate(my_books):
#         if b['id'] == id:
#             return i
