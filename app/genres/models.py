from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.db import Base


class Genres(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, nullable=False)
    genre_name = Column(String, nullable=False)

    book = relationship("Books", back_populates="genre")

    def __str__(self):
        return f"Customer: {self.genre_name}"
