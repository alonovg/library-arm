from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from app.database.db import Base


class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, nullable=False)
    customer_full_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    address = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    book_transaction = relationship("BookTransactions", back_populates="customer")

    def __str__(self):
        return f"Customer: {self.customer_full_name}"
