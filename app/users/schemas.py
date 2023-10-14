from pydantic import BaseModel, EmailStr, Field


class SUserAuth(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class SUserUpdate(BaseModel):
    email: EmailStr = Field(None, description="Новый Email пользователя")
    password: str = Field(None, description="Новый пароль пользователя")

    class Config:
        from_attributes = True
