from datetime import date, timedelta

from fastapi import APIRouter, Depends

from app.book_transactions.dao import BookTransactionDAO
from app.book_transactions.schemas import SBookTransactionAdd
from app.books.dao import BookDAO
from app.customers.dao import CustomerDAO
from app.exceptions import (CannotFindBook,
                            CannotFindCustomer,
                            CannotFindBookTransaction,
                            BookAlreadyBusyException)
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix="/books-transactions",
    tags=["Движения книг"]
)


@router.get("")
async def get_transactions(user: Users = Depends(get_current_user)):
    """Получает список всех операций по книгам"""
    return await BookTransactionDAO.find_all()


async def get_transactions_joined(user: Users = Depends(get_current_user)):
    """Получение JOIN таблиц для подзагрузки SQLAlchemy"""
    return await BookTransactionDAO.get_transactions_info()


@router.post("", status_code=201)
async def add_transaction(transaction: SBookTransactionAdd, user: Users = Depends(get_current_user)):
    """Добавляет новую операцию по книге"""
    find_book = await BookDAO.find_one_or_none(id=transaction.book_id)
    if not find_book:
        raise CannotFindBook
    if not find_book.availability:
        raise BookAlreadyBusyException
    find_customer = CustomerDAO.find_one_or_none(id=transaction.customer_id)
    if not find_customer:
        raise CannotFindCustomer
    await BookDAO.update(transaction.book_id, {"availability": False})
    expected_return_date = date.today() + timedelta(days=30)
    return await BookTransactionDAO.add(
        book_id=transaction.book_id,
        customer_id=transaction.customer_id,
        transaction_date=date.today(),
        expected_return_date=expected_return_date,
        returned_date=None
    )


@router.patch("/{transaction_id}", status_code=200)
async def update_transaction_by_id(transaction_id: int):
    """Обновляет информацию о возвращении книги по ID операции"""
    find_transaction = await BookTransactionDAO.find_one_or_none(id=transaction_id)
    if not find_transaction:
        raise CannotFindBookTransaction
    await BookDAO.update(find_transaction.book_id, {"availability": True})
    return await BookTransactionDAO.update(transaction_id, {"returned_date": date.today()})


@router.patch("", status_code=200)
async def update_transaction_by_customer_book_id(transaction: SBookTransactionAdd):
    """Обновляет информацию о возвращении книги по ID читателя и ID книги"""
    find_transaction = await BookTransactionDAO.find_one_or_none(
        book_id=transaction.book_id,
        customer_id=transaction.customer_id,
        returned_date=None)
    if not find_transaction:
        raise CannotFindBookTransaction
    await BookDAO.update(transaction.book_id, {"availability": True})
    return await BookTransactionDAO.update(find_transaction.id, {"returned_date": date.today()})


@router.delete("/{transaction_id}", status_code=204)
async def transaction_delete(transaction_id: int, user: Users = Depends(get_current_user)):
    """Удаляет операцию по ID"""
    find_transaction = await BookTransactionDAO.find_one_or_none(id=transaction_id)
    if not find_transaction:
        raise CannotFindBookTransaction
    if not find_transaction.returned_date:
        await BookDAO.update(find_transaction.book_id, {"availability": True})
    return await BookTransactionDAO.delete(id=transaction_id)


@router.get("/report")
async def get_report_about_transactions(user: Users = Depends(get_current_user)):
    return await BookTransactionDAO.get_reports()
