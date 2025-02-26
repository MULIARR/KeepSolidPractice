from fastapi import APIRouter, Depends, HTTPException
from typing import List
import csv
import io

from app.core.security import get_current_user
from app.dto.book import BookRead, BookCreate
from constants import Role
from database import db
from database.schema import User

books_router = APIRouter(tags=["books"])


@books_router.get("/books", response_model=List[BookRead])
async def get_all_books():
    """
    :return: list of Book
    """
    books = await db.book.get_all_books()
    return books  # Pydantic сам применит BookRead(orm_mode=True)


@books_router.get("/books/{book_id}", response_model=BookRead)
async def get_book_by_id(
    book_id: int
):
    """
    :return: specific Book data
    """
    book = await db.book.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@books_router.post("/books", response_model=BookRead)
async def create_book(
    book_data: BookCreate,
    current_user: User = Depends(get_current_user)
):
    """
    New Book creation (ROLE=ADMIN).
    takes arguments: title, list author_ids and genre_ids.
    """
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can create books")

    created_book = await db.book.create_book(title=book_data.title)
    if book_data.author_ids:
        await db.book.link_authors_to_book(created_book.book_id, book_data.author_ids)
    if book_data.genre_ids:
        await db.book.link_genres_to_book(created_book.book_id, book_data.genre_ids)

    new_book = await db.book.get_book_by_id(created_book.book_id)
    return new_book


@books_router.delete("/books/{book_id}")
async def delete_book(
    book_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Book deletion (ROLE=ADMIN).
    """
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can delete books")

    book = await db.book.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await db.book.delete_book(book_id)
    return {"detail": f"Book {book_id} has been deleted."}


@books_router.post("/favorites/{book_id}")
async def add_favorite_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
):
    """
    Book to favorites addition
    """
    book = await db.book.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await db.user.add_book_to_favorites(current_user.user_id, book_id)
    return {"detail": f"Book {book_id} added to favorites."}


@books_router.delete("/favorites/{book_id}")
async def remove_favorite_book(
    book_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Book from favorites deletion
    """
    book = await db.book.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await db.user.remove_book_from_favorites(current_user.user_id, book_id)
    return {"detail": f"Book {book_id} removed from favorites."}


from fastapi.responses import Response


@books_router.get("/books/export")
async def export_books_to_csv(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can export books")

    books = await db.book.get_all_books()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["book_id", "title", "authors", "genres"])

    for book in books:
        authors_str = ", ".join([a.name for a in book.authors])
        genres_str = ", ".join([g.name for g in book.genres])
        writer.writerow([book.book_id, book.title, authors_str, genres_str])

    csv_data = output.getvalue()

    return Response(content=csv_data, media_type="text/csv")
