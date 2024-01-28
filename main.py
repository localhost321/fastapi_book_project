from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Depends

from schema import BookSchema as SchemaBook, BookCreate, AuthorReadModel, AuthorCreateModel, BookUpdate, \
    AuthorBooksModel
from sqlmodel import Session, create_engine, select

from models import Book as ModelBook, Book
from models import Author as ModelAuthor

import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

# to avoid csrftokenError
engine = create_engine(os.environ['DATABASE_URL'])


def get_session():
    with Session(engine) as session:
        yield session


# index
@app.get("/")
async def root():
    return {"message": "hello world"}


# create book
@app.post('/book/', response_model=SchemaBook)
async def book(*, session: Session = Depends(get_session), book: BookCreate):
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


# book detail
@app.patch('/book/{book_id}', response_model=BookCreate)
async def book(*, session: Session = Depends(get_session), book_id: int, book: BookUpdate):
    # db_book = select(ModelBook).where(ModelBook.id == book_id)
    db_book = session.get(ModelBook, book_id)
    if db_book is None:
        return HTTPException(status_code=404, detail="Book not found")
    book_data = book.model_dump(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


# delete book
@app.delete('/book/{book_id}')
async def book(*, session: Session = Depends(get_session), book_id: int):
    db_book = session.get(ModelBook, book_id)
    if not db_book:
        return HTTPException(status_code=404, detail="Book not found")
    session.delete(db_book)
    session.commit()
    return {"message": "book delete successfully"}


# book list
@app.get('/book/', response_model=List[ModelBook])
async def book(*, session: Session = Depends(get_session), page_offset: int = 0,
               limit: int = Query(default=100, le=100)):
    books_data = select(ModelBook).offset(page_offset).limit(limit)
    book_data = session.exec(books_data).all()
    return book_data


# book detail api
@app.get('/book/{book_id}', response_model=SchemaBook)
async def book(*, session: Session = Depends(get_session), book_id: int):
    books_data = select(ModelBook).where(ModelBook.id == book_id)
    book_data = session.exec(books_data).first()
    if book_data is None:
        raise HTTPException(status_code=404, detail="Book detail not found")
    return book_data


# create author
@app.post('/author/', response_model=AuthorReadModel)
async def author(*, session: Session = Depends(get_session), author: AuthorCreateModel):
    db_author = ModelAuthor.model_validate(author)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


# author list
@app.get('/author/', response_model=List[ModelAuthor])
async def author(*, session: Session = Depends(get_session), page_offset: int = 0,
                 limit: int = Query(default=100, le=100)):
    author_data = select(ModelAuthor).offset(page_offset).limit(limit)
    authors_detail = session.exec(author_data).all()
    return authors_detail


# author details
@app.get('/author/{author_id}/', response_model=AuthorBooksModel)
async def author(*, session: Session = Depends(get_session), author_id: int):
    author_data = session.get(ModelAuthor, author_id)
    return author_data


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
