from pydantic import BaseModel, Field


class SBookTransactionAdd(BaseModel):
    book_id: int = Field(..., description="ID книги")
    customer_id: int = Field(..., description="ID пользователя")

    class Config:
        from_attributes = True
