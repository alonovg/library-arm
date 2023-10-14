from sqlalchemy import select, and_, or_, desc, func
from sqlalchemy.orm import joinedload

from app.book_transactions.models import BookTransactions
from app.books.models import Books
from app.dao.base import BaseDAO
from app.database.db import async_session_maker


class BookDAO(BaseDAO):
    model = Books

    @classmethod
    async def find_book_by_id(cls, book_id: int):
        """
        SELECT *
        FROM book_transactions
        WHERE book_id = 1
        ORDER BY id DESC
        LIMIT 1;
        """
        query = select(BookTransactions).filter(
            BookTransactions.book_id == book_id
        ).order_by(BookTransactions.id.desc())
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.mappings().first()

    @classmethod
    async def find_most_readers_book(cls):
        """
        SELECT book_id, COUNT(book_id) as count
        FROM (
            SELECT book_id
            FROM book_transactions
        ) AS subquery
        GROUP BY book_id
        ORDER BY count DESC
        LIMIT 1;
        """
        sub_query = select(BookTransactions.book_id).subquery()

        query = select(sub_query.c.book_id, func.count(sub_query.c.book_id).label('count')).group_by(
            sub_query.c.book_id
        ).order_by(
            func.count(sub_query.c.book_id).desc()
        ).limit(1)
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def get_book_info(cls):
        """
        SELECT *
        FROM books
        JOIN authors ON authors.id = books.author_id
        JOIN genres ON genres.id = books.genre_id;
        """
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(cls.model.author), joinedload(cls.model.genre))
            results = await session.execute(query)
            if results:
                return results.scalars().all()
            return "Unknown book_data"
