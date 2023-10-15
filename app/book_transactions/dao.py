from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.authors.models import Authors
from app.book_transactions.models import BookTransactions
from app.dao.base import BaseDAO
from app.database.db import async_session_maker


class BookTransactionDAO(BaseDAO):
    model = BookTransactions

    @classmethod
    async def get_transactions_info(cls):
        """
        SELECT *
        FROM book_transactions
        JOIN books ON books.id = book_transactions.book_id
        JOIN customers ON customers.id = book_transactions.customer_id;
        """
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(cls.model.book), joinedload(cls.model.customer))
            results = await session.execute(query)
            if results:
                return results.scalars().all()
            return "Unknown book_transaction_data"

    @classmethod
    async def get_reports(cls):
        # 1. expected_return_date уже в прошедшем времени и returned_date == None
        condition_1 = (BookTransactions.expected_return_date < date.today()) & (BookTransactions.returned_date == None)
        # 2. returned_date больше, чем expected_return_date
        condition_2 = BookTransactions.returned_date > BookTransactions.expected_return_date
        query = select(cls.model).filter(condition_1 | condition_2).options(
            joinedload(cls.model.book), joinedload(cls.model.customer))
        async with async_session_maker() as session:
            results = await session.execute(query)
            return results.scalars().all()


