from pydantic import BaseModel, Field
from datetime import date


class SCustomer(BaseModel):
    customer_full_name: str
    date_of_birth: date
    address: str
    phone_number: str

    class Config:
        from_attributes = True


class SCustomerUpdate(BaseModel):
    customer_full_name: str = Field(None, description="ФИО, например: Иванов Иван Иванович")
    date_of_birth: date = Field(None, description="Дата рождения, например: 1995-10-13")
    address: str = Field(None, description="Адрес, например: г. Москва, ул. Южная, д. 295")
    phone_number: str = Field(None, description="Номер тел.: +79920939872")

    class Config:
        from_attributes = True
