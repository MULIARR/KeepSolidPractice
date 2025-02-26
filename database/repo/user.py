from sqlalchemy import select, exists

from constants import Role
from database.base import BaseRepository
from database.schema import User, UserFavorite


class UserRepository(BaseRepository):
    async def create_user(self, email: str, hashed_password: str, role: Role = Role.USER) -> User:
        async with self.session_local() as session:
            user = User(
                email=email,
                hashed_password=hashed_password,
                role=role
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def update_user_role(self, user_id: int, role: Role) -> bool:
        async with self.session_local() as session:
            user = await session.get(User, user_id)

            if not user:
                return False

            user.role = role
            await session.commit()
            return True

    async def get_user_by_id(self, user_id: int) -> User | None:
        async with self.session_local() as session:
            result = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        async with self.session_local() as session:
            result = await session.execute(
                select(User).where(User.email == email)
            )
            return result.scalar_one_or_none()

    async def user_exists(self, user_id: int) -> bool:
        async with self.session_local() as session:
            stmt = select(exists().where(User.user_id == user_id))
            result = await session.execute(stmt)
            return result.scalar()

    async def update_role(self, user_id: int, new_role: Role) -> None:
        async with self.session_local() as session:
            user = await session.get(User, user_id)
            if user:
                user.role = new_role
                await session.commit()

    async def add_book_to_favorites(self, user_id: int, book_id: int) -> None:
        async with self.session_local() as session:
            stmt = select(UserFavorite).where(
                UserFavorite.user_id == user_id,
                UserFavorite.book_id == book_id
            )
            result = await session.execute(stmt)
            fav = result.scalar_one_or_none()

            if not fav:
                fav = UserFavorite(
                    user_id=user_id,
                    book_id=book_id
                )
                session.add(fav)
                await session.commit()

    async def remove_book_from_favorites(self, user_id: int, book_id: int) -> None:
        async with self.session_local() as session:
            stmt = select(UserFavorite).where(
                UserFavorite.user_id == user_id,
                UserFavorite.book_id == book_id
            )
            result = await session.execute(stmt)
            fav = result.scalar_one_or_none()

            if fav:
                await session.delete(fav)
                await session.commit()
