from config import config
from database.base import get_engine, get_session_local, Base

from .repo import (
    UserRepository,
    AuthorRepository,
    BookRepository,
    GenreRepository
)


class Database:
    def __init__(self, database_url: str):
        self.engine = get_engine(database_url)
        self.session_local = get_session_local(self.engine)

        self.user = UserRepository(self.session_local)
        self.author = AuthorRepository(self.session_local)
        self.book = BookRepository(self.session_local)
        self.genre = GenreRepository(self.session_local)

    async def async_init(self):
        async with self.engine.begin() as conn:
            ...
            # await conn.run_sync(Base.metadata.drop_all)
            # await conn.run_sync(Base.metadata.create_all)

    async def close(self):
        self.session_local.close_all()


db = Database(config.db.database_url)

# import all models (native import)
import database.schema
