from .user import User
from .author import Author
from .book import Book
from .genre import Genre
from .m2m import BookAuthor, BookGenre, UserFavorite

__all__ = [
    "User",
    "Author",
    "Book",
    "Genre",
    "BookAuthor",
    "BookGenre",
    "UserFavorite"
]
