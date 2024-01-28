# build a schema using sqlmodel
from sqlmodel import SQLModel
from typing import Optional, List


# Book Pydantic Model
class BookBaseModel(SQLModel):
    title: str
    rating: float


class BookUpdate(SQLModel):
    title: Optional[str] = None
    rating: Optional[float] = None
    author_id: Optional[int] = None


class BookCreate(BookBaseModel):
    pass


# Author Pydantic Model
class AuthorBaseModel(SQLModel):
    name: str
    age: int



class AuthorReadModel(AuthorBaseModel):
    pass

class BookSchema(BookBaseModel):
    id: int
    author: Optional[AuthorReadModel]


class AuthorCreateModel(AuthorReadModel):
    id: int


class AuthorBooksModel(AuthorBaseModel):
    books_data: List[BookSchema]
