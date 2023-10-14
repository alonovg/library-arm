from pydantic import BaseModel, Field


class SBook(BaseModel):
    title: str = Field(..., description="Название книги")
    author_id: int = Field(..., description="ID автора книги")
    genre_id: int = Field(..., description="ID жанра")

    class Config:
        from_attributes = True


class SBookUpdate(BaseModel):
    title: str = Field(None, description="Название книги")
    author_id: int = Field(None, description="ID автора книги")
    availability: bool = Field(None, description="True - в библиотеке, False - нет")
    genre_id: int = Field(None, description="ID жанра")

    class Config:
        from_attributes = True
