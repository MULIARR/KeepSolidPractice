from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.async_init()

    books = await db.book.get_all_books()
    for book in books:
        print(book.__dict__)

    yield

    await db.close()
