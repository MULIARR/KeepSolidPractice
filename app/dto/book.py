from pydantic import BaseModel
from typing import List


class BookCreate(BaseModel):
    title: str
    author_ids: List[int] = []
    genre_ids: List[int] = []


class AuthorRead(BaseModel):
    author_id: int
    name: str

    class Config:
        from_attributes = True


class GenreRead(BaseModel):
    genre_id: int
    name: str

    class Config:
        from_attributes = True


class BookRead(BaseModel):
    book_id: int
    title: str
    authors: List[AuthorRead] = []
    genres: List[GenreRead] = []

    class Config:
        from_attributes = True
