from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.base import BaseRepository
from database.schema import Book, BookAuthor, BookGenre


class BookRepository(BaseRepository):
    async def create_book(self, title: str) -> Book:
        async with self.session_local() as session:
            book = Book(title=title)
            session.add(book)
            await session.commit()
            await session.refresh(book)
            return book

    async def get_book_by_id(self, book_id: int) -> Book | None:
        async with self.session_local() as session:
            result = await session.execute(
                select(Book)
                .options(
                    selectinload(Book.authors),
                    selectinload(Book.genres)
                )
                .where(Book.book_id == book_id)
            )
            return result.scalar_one_or_none()

    async def get_all_books(self) -> list[Book]:
        async with self.session_local() as session:
            stmt = (
                select(Book)
                .options(
                    selectinload(Book.authors),
                    selectinload(Book.genres)
                )
            )
            result = await session.execute(stmt)
            books = result.scalars().all()
            return books

    async def delete_book(self, book_id: int) -> None:
        async with self.session_local() as session:
            book = await session.get(Book, book_id)
            if book:
                await session.delete(book)
                await session.commit()

    async def link_authors_to_book(self, book_id: int, author_ids: list[int]) -> None:
        """
        link list author_ids to Book
        """
        if not author_ids:
            return

        async with self.session_local() as session:
            for author_id in author_ids:
                stmt = select(BookAuthor).where(
                    BookAuthor.book_id == book_id,
                    BookAuthor.author_id == author_id
                )
                existing_link = await session.execute(stmt)
                if not existing_link.scalar_one_or_none():
                    link = BookAuthor(book_id=book_id, author_id=author_id)
                    session.add(link)

            await session.commit()

    async def link_genres_to_book(self, book_id: int, genre_ids: list[int]) -> None:
        """
        link list genre_ids to Book
        """
        if not genre_ids:
            return

        async with self.session_local() as session:
            for genre_id in genre_ids:
                stmt = select(BookGenre).where(
                    BookGenre.book_id == book_id,
                    BookGenre.genre_id == genre_id
                )
                existing_link = await session.execute(stmt)
                if not existing_link.scalar_one_or_none():
                    link = BookGenre(book_id=book_id, genre_id=genre_id)
                    session.add(link)

            await session.commit()
