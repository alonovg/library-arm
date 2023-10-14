from fastapi import APIRouter, Depends

from app.authors.dao import AuthorDAO
from app.books.dao import BookDAO
from app.books.schemas import SBook, SBookUpdate
from app.exceptions import CannotFindBook, CannotFindAuthor, CannotFindGenre
from app.genres.dao import GenreDAO
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix="/books",
    tags=["Книги"]
)


@router.get("")
async def get_books():
    """Получает список книг"""
    return await BookDAO.find_all()


async def get_books_joined(user: Users = Depends(get_current_user)):
    """Получение JOIN таблиц для подзагрузки SQLAlchemy"""
    return await BookDAO.get_book_info()


@router.get("/{book_id}")
async def get_book_by_id(book_id: int):
    """Получение книги по ID"""
    return await BookDAO.find_one_or_none(id=book_id)


@router.post("", status_code=201)
async def add_book(book: SBook, user: Users = Depends(get_current_user)):
    """Добавление книги"""
    find_author = await AuthorDAO.find_one_or_none(id=book.author_id)
    if not find_author:
        raise CannotFindAuthor
    find_genre = await GenreDAO.find_one_or_none(id=book.genre_id)
    if not find_genre:
        raise CannotFindGenre
    book = await BookDAO.add(
        title=book.title,
        author_id=book.author_id,
        availability=True,
        genre_id=book.genre_id,
    )
    return book


@router.patch("/{book_id}", status_code=200)
async def update_book(book_id: int, book_data: SBookUpdate, user: Users = Depends(get_current_user)):
    """Обновление информации о книге"""
    find_book = await BookDAO.find_one_or_none(id=book_id)
    if not find_book:
        raise CannotFindBook
    filled_fields = {}
    if book_data.title and find_book.title != book_data.title:
        filled_fields['title'] = book_data.title
    if book_data.author_id and find_book.author_id != book_data.author_id:
        filled_fields['author_id'] = book_data.author_id
    if book_data.availability and find_book.author_id != book_data.availability:
        filled_fields['availability'] = book_data.availability
    if book_data.genre_id and find_book.author_id != book_data.genre_id:
        filled_fields['genre_id'] = book_data.genre_id
    if not filled_fields:
        return {"message": "Данные не были изменены"}
    await BookDAO.update(book_id, values=filled_fields)
    return {"message": "Книга успешно обновлена"}


@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: int, user: Users = Depends(get_current_user)):
    """Удаление книги по ID"""
    find_book = await BookDAO.find_one_or_none(id=book_id)
    if not find_book:
        raise CannotFindBook
    await BookDAO.delete(id=book_id)


@router.get("/find/{book_id}")
async def look_for_book(book_id: int, user: Users = Depends(get_current_user)):
    """Поиск местонахождения книги"""
    find_book = await BookDAO.find_one_or_none(id=book_id)
    if find_book.availability:
        return {"message": "Книга в библиотеке"}
    return await BookDAO.find_book_by_id(book_id)


@router.get("/mvp/book")
async def get_mvp_book():
    """Получает самую читаемую книгу"""
    result = await BookDAO.find_most_readers_book()
    if result:
        book_id = result[0].book_id
        return await BookDAO.find_one_or_none(id=book_id)
