from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database.db import Base


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    author_id = Column(ForeignKey("authors.id"))
    availability = Column(Boolean, nullable=False)
    genre_id = Column(ForeignKey("genres.id"))

    author = relationship("Authors", back_populates="book")
    genre = relationship("Genres", back_populates="book")
    book_transaction = relationship("BookTransactions", back_populates="book")

    def __str__(self):
        return f"Book: {self.title}"
