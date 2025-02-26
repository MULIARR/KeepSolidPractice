from sqlalchemy import select

from database.base import BaseRepository
from database.schema import Author


class AuthorRepository(BaseRepository):
    async def create_author(self, name: str) -> Author:
        async with self.session_local() as session:
            author = Author(name=name)
            session.add(author)
            await session.commit()
            await session.refresh(author)
            return author

    async def get_author_by_id(self, author_id: int) -> Author | None:
        async with self.session_local() as session:
            result = await session.execute(
                select(Author).where(Author.author_id == author_id)
            )
            return result.scalar_one_or_none()

    async def get_all_authors(self) -> list[Author]:
        async with self.session_local() as session:
            result = await session.execute(select(Author))
            return result.scalars().all()

    async def delete_author(self, author_id: int) -> None:
        async with self.session_local() as session:
            author = await session.get(Author, author_id)
            if author:
                await session.delete(author)
                await session.commit()
