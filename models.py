from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime

from schema import BookBaseModel




# using fastapi sqlmodel orm library


class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    time_created: datetime = Field(default=datetime.utcnow(), nullable=False)
    time_updated: datetime = Field(default=datetime.utcnow(), nullable=False)
    books_data: List["Book"] = Relationship(back_populates="author")


class Book(BookBaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    time_created: datetime = Field(default=datetime.utcnow(), nullable=False)
    time_updated: datetime = Field(default=datetime.utcnow(), nullable=False)
    author_id: int = Field(default=None, foreign_key="author.id")
    author: Author = Relationship(back_populates="books_data")





