from fastapi import APIRouter, Depends

from app.exceptions import CannotFindGenre, GenreAlreadyExistException
from app.genres.dao import GenreDAO
from app.genres.schemas import SGenre
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/genres",
    tags=["Жанры"]
)


@router.get("")
async def get_genres():
    """Получает список жанров"""
    return await GenreDAO.find_all()


@router.post("", status_code=201)
async def add_genre(genre: SGenre):
    """Добавляет новый жанр"""
    find_genre = GenreDAO.find_one_or_none(genre_name=genre.genre_name)
    if find_genre:
        raise GenreAlreadyExistException
    return await GenreDAO.add(genre_name=genre.genre_name)


@router.delete("/{author_id}", status_code=204)
async def genre_delete(genre_id: int, user: Users = Depends(get_current_user)):
    """Удаляет жанр по ID"""
    find_genre_id = GenreDAO.find_one_or_none(id=genre_id)
    if not find_genre_id:
        raise CannotFindGenre
    return await GenreDAO.delete(id=genre_id)


@router.get("/mvp/genre")
async def get_mvp_genre():
    """Получение самого популярного жарна"""
    result = await GenreDAO.get_most_genre()
    if not result:
        raise CannotFindGenre
    return result
