from fastapi import APIRouter, Depends, Response
from starlette.responses import JSONResponse

from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.exceptions import CannotAddDataToDatabase, UserAlreadyExistsException
from app.users.schemas import SUserAuth


router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

router_users = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@router_users.get("/me")
async def read_user_me(current_user: Users = Depends(get_current_user)):
    """Получение текущего пользователя"""
    return current_user


@router_auth.post("/register", status_code=201)
async def register_user(user: SUserAuth):
    """Регистрация пользователя"""
    existing_user = await UserDAO.find_one_or_none(email=user.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user.password)
    new_user = await UserDAO.add(email=user.email, hashed_password=hashed_password)
    if not new_user:
        raise CannotAddDataToDatabase
    return JSONResponse(content={"message": "Пользователь успешно зарегистрирован",
                                 "email": user.email})


@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    """Аутентификация пользователя"""
    user = await authenticate_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("library_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router_auth.post("/logout")
async def logout_user(response: Response):
    """Выход пользователя - удаление куки"""
    response.delete_cookie("library_access_token")


