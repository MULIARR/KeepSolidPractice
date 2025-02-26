from sqlalchemy import select

from database.base import BaseRepository
from database.schema import Genre


class GenreRepository(BaseRepository):
    async def create_genre(self, name: str) -> Genre:
        async with self.session_local() as session:
            genre = Genre(name=name)
            session.add(genre)
            await session.commit()
            await session.refresh(genre)
            return genre

    async def get_genre_by_id(self, genre_id: int) -> Genre | None:
        async with self.session_local() as session:
            result = await session.execute(
                select(Genre).where(Genre.genre_id == genre_id)
            )
            return result.scalar_one_or_none()

    async def get_all_genres(self) -> list[Genre]:
        async with self.session_local() as session:
            result = await session.execute(select(Genre))
            return result.scalars().all()

    async def delete_genre(self, genre_id: int) -> None:
        async with self.session_local() as session:
            genre = await session.get(Genre, genre_id)
            if genre:
                await session.delete(genre)
                await session.commit()
