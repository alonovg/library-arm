from fastapi import APIRouter, Depends

from app.authors.dao import AuthorDAO
from app.authors.schemas import SAuthor
from app.exceptions import CannotFindAuthor, AuthorAlreadyExistException
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix="/authors",
    tags=["Авторы книг"]
)


@router.get("")
async def get_authors():
    """Получает список всех авторов"""
    return await AuthorDAO.find_all()


@router.post("", status_code=201)
async def add_author(author: SAuthor, user: Users = Depends(get_current_user)):
    """Добавляет автора"""
    find_author = AuthorDAO.find_one_or_none(author_full_name=author.author_full_name)
    if find_author:
        raise AuthorAlreadyExistException
    return await AuthorDAO.add(author_full_name=author.author_full_name)


@router.delete("/{author_id}", status_code=204)
async def author_delete(author_id: int, user: Users = Depends(get_current_user)):
    """Удаляет автора"""
    find_author = AuthorDAO.find_one_or_none(id=author_id)
    if not find_author:
        raise CannotFindAuthor
    return await AuthorDAO.delete(id=author_id)


@router.get("mvp/author")
async def get_mvp_author():
    """Получает самого читаемого автора"""
    result = await AuthorDAO.get_most_read_author()
    if result:
        return result[0].id
