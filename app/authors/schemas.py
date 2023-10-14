from pydantic import BaseModel, Field


class SAuthor(BaseModel):
    author_full_name: str = Field(..., description="Полное имя автора")

    class Config:
        from_attributes = True
