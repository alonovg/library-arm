from pydantic import BaseModel, Field


class SGenre(BaseModel):
    genre_name: str = Field(..., description="Название жанра")

    class Config:
        from_attributes = True