from sqlalchemy import select, func

from app.authors.models import Authors
from app.book_transactions.models import BookTransactions
from app.books.models import Books
from app.dao.base import BaseDAO
from app.database.db import async_session_maker


class AuthorDAO(BaseDAO):
    model = Authors

    @classmethod
    async def get_most_read_author(cls):
        """
        SELECT authors.id as author_id, COUNT(book_transactions.id) as read_count
        FROM authors
        JOIN books ON authors.id = books.author_id
        JOIN book_transactions ON books.id = book_transactions.book_id
        GROUP BY authors.id
        ORDER BY read_count DESC
        LIMIT 1;
        """
        query = select(Authors.id, func.count(BookTransactions.id).label('read_count')).join(
            Books, Authors.id == Books.author_id).join(
            BookTransactions, Books.id == BookTransactions.book_id).group_by(
            Authors.id).order_by(func.count(BookTransactions.id).desc()).limit(1)
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.mappings().all()
