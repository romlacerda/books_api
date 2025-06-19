from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
        
        
class BookRequest(BaseModel):
    id: Optional[int] = Field(title="Id is not needed")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=3000)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Computer Science Pro",
                "author": "codingwithroby",
                "description": "A very nice book",
                "rating": 5,
                "published_date": 2022
            }
        }
    }
    
    
        
BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book', 5, 2015),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book', 5, 2022),
    Book(3, 'Master Endpoints', 'codingwithroby', 'Good', 5, 1999),
    Book(4, 'React with Reactions', 'codingwithroby', 'Awesome', 3, 1998),
    Book(5, 'HP2', 'JK Rowling', 'Nothing special', 4, 2001),
    Book(6, 'Lord of the Rings', 'Tolkien', 'A very nice book', 5, 1823),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
        
    raise HTTPException(status_code=404, detail="Book does not exist.")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.post("/books/", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookRequest):
    new_book = Book(**book.model_dump())
    BOOKS.append(find_book_id(new_book))
    return new_book
    
    
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.put("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest, book_id: int):
    book_changed = False
    
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            print(BOOKS[i])
            BOOKS[i] = book
            BOOKS[i].id = book_id
            book_changed = True

    if not book_changed:
        raise HTTPException(status_code=404, detail="Book does not exist.")
            
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    print(book_id)
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            print(BOOKS[i])
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book does not exist.")   
        
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: int = Query(gt=1999, lt=3000)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return