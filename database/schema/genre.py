from sqlalchemy import BigInteger, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.base import Base


class Genre(Base):
    __tablename__ = "genres"

    genre_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # many-to-many: Genre -> Book
    books: Mapped[list["Book"]] = relationship(
        secondary="book_genres",
        back_populates="genres"
    )
