from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database.db import Base


class BookTransactions(Base):
    __tablename__ = "book_transactions"

    id = Column(Integer, primary_key=True, nullable=False)
    book_id = Column(ForeignKey("books.id"))
    customer_id = Column(ForeignKey("customers.id"))
    transaction_date = Column(Date, nullable=False)
    expected_return_date = Column(Date, nullable=False)
    returned_date = Column(Date, nullable=True)

    book = relationship("Books", back_populates="book_transaction")
    customer = relationship("Customers", back_populates="book_transaction")

    def __str__(self):
        return f"Transaction #{self.id}"
