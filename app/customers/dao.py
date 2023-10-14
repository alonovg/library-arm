from sqlalchemy import select

from app.book_transactions.models import BookTransactions
from app.customers.models import Customers
from app.dao.base import BaseDAO
from app.database.db import async_session_maker


class CustomerDAO(BaseDAO):
    model = Customers

    @classmethod
    async def get_last_visit_date(cls, customer_id: int):
        """
        SELECT *
        FROM book_transactions
        WHERE customer_id = 1
        ORDER BY id DESC
        LIMIT 1;
        """
        query = select(BookTransactions).filter(
            BookTransactions.customer_id == customer_id
        ).order_by(BookTransactions.id.desc())
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.scalars().first()

