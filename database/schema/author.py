from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Author(Base):
    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # many-to-many: Author -> Book
    books: Mapped[list["Book"]] = relationship(
        secondary="book_authors",
        back_populates="authors"
    )
