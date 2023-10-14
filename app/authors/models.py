from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.db import Base


class Authors(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, nullable=False)
    author_full_name = Column(String, nullable=False)

    book = relationship("Books", back_populates="author")

    def __str__(self):
        return f"Author: {self.author_full_name}"
