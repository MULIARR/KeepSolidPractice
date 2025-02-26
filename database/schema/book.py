from datetime import datetime

from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Book(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # many-to-many: Book -> Author
    authors: Mapped[list["Author"]] = relationship(
        secondary="book_authors",
        back_populates="books"
    )

    # many-to-many: Book -> Genre
    genres: Mapped[list["Genre"]] = relationship(
        secondary="book_genres",
        back_populates="books"
    )

    favorite_by_users: Mapped[list["User"]] = relationship(
        secondary="user_favorites",
        back_populates="favorites"
    )
