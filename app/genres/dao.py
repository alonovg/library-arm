from sqlalchemy import select, func

from app.book_transactions.models import BookTransactions
from app.books.models import Books
from app.customers.models import Customers
from app.dao.base import BaseDAO
from app.database.db import async_session_maker
from app.genres.models import Genres


class GenreDAO(BaseDAO):
    model = Genres

    @classmethod
    async def get_most_genre(cls):
        """
        SELECT genres.genre_name, COUNT(book_transactions.id) as preference_count  --Comments: (or genres.id)
        FROM genres
        JOIN books ON genres.id = books.genre_id
        JOIN book_transactions ON books.id = book_transactions.book_id
        GROUP BY genres.genre_name  --Comments: (or genres.id)
        ORDER BY preference_count DESC;
        """
        query = select(Genres.genre_name, func.count(BookTransactions.id).label('preference_count')).join(
            Books, Genres.id == Books.genre_id).join(
            BookTransactions, Books.id == BookTransactions.book_id).group_by(
            Genres.genre_name).order_by(func.count(BookTransactions.id).desc())
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.scalars().all()
