from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional

db_client = MongoClient("mongodb://localhost:27017/")
db = db_client.bookstore
collection = db.books

app = FastAPI()

class Book(BaseModel):
    title: str
    price: float
    availability: bool
    rating: int
    url: str

@app.get("/books", response_model=List[Book])
def get_books(rating: Optional[int] = None, available: Optional[bool] = None):
    query = {}
    if rating is not None:
        query["rating"] = rating
    if available is not None:
        query["availability"] = available
    books = list(collection.find(query, {"_id": 0}))
    return books

@app.post("/books", response_model=Book)
def create_book(book: Book):
    collection.insert_one(book.dict())
    return book

@app.put("/books/{title}", response_model=Book)
def update_book(title: str, book: Book):
    result = collection.update_one({"title": title}, {"$set": book.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not found in the book store")
    return book

@app.delete("/books/{title}")
def delete_book(title: str):
    result = collection.delete_one({"title": title})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found in the book store")
    return {"message": f"Deleted book '{title}'"}
