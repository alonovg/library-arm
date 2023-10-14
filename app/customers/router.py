from collections import Counter

from fastapi import APIRouter, Depends

from app.book_transactions.dao import BookTransactionDAO
from app.books.dao import BookDAO
from app.customers.dao import CustomerDAO
from app.customers.schemas import SCustomer, SCustomerUpdate
from app.exceptions import CannotFindCustomer
from app.genres.dao import GenreDAO
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/customers",
    tags=["Читатели"]
)


@router.get("")
async def get_customers(user: Users = Depends(get_current_user)):
    """Получение всех читателей"""
    return await CustomerDAO.find_all()


@router.get("/{customer_id}")
async def get_customer_by_id(customer_id: int, user: Users = Depends(get_current_user)):
    """Получение читателя по ID"""
    return await CustomerDAO.find_one_or_none(id=customer_id)


@router.post("")
async def add_customer(customer: SCustomer, user: Users = Depends(get_current_user)):
    """Добавление читателя"""
    return await CustomerDAO.add(
        customer_full_name=customer.customer_full_name,
        date_of_birth=customer.date_of_birth,
        address=customer.address,
        phone_number=customer.phone_number
    )


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(customer_id: int, user: Users = Depends(get_current_user)):
    """Удаление читателя по ID"""
    find_customer = await CustomerDAO.find_one_or_none(id=customer_id)
    if not find_customer:
        raise CannotFindCustomer
    await CustomerDAO.delete(id=customer_id)


@router.patch("/{customer_id}", status_code=200)
async def update_customer(customer_id: int, customer: SCustomerUpdate, user: Users = Depends(get_current_user)):
    """Обновление информации о читателе"""
    find_customer = await CustomerDAO.find_one_or_none(id=customer_id)
    if not find_customer:
        raise CannotFindCustomer
    filled_fields = {}
    if customer.customer_full_name and customer.customer_full_name != find_customer.customer_full_name:
        filled_fields["customer_full_name"] = customer.customer_full_name
    if customer.date_of_birth and customer.date_of_birth != find_customer.date_of_birth:
        filled_fields["date_of_birth"] = customer.date_of_birth
    if customer.address and customer.address != find_customer.address:
        filled_fields["address"] = customer.address
    if customer.phone_number and customer.phone_number != find_customer.phone_number:
        filled_fields["phone_number"] = customer.phone_number
    if not filled_fields:
        return {"message": "Нет новых данных для обновления"}
    await CustomerDAO.update(customer_id, values=filled_fields)
    return {"message": "Пользователь успешно обновлен"}


@router.get("/book-count/all-time/{customer_id}")
async def get_count_book_all_time(customer_id: int):
    """Получение кол-ва книг, взятых читателем за все время"""
    find_customer = await CustomerDAO.find_one_or_none(id=customer_id)
    if not find_customer:
        raise CannotFindCustomer
    return await BookTransactionDAO.find_all(customer_id=customer_id)


@router.get("/book-count/right-not/{customer_id}")
async def get_count_book_at_the_moment(customer_id: int):
    """Получение кол-ва книг, которые читатель еще не вернул"""
    find_customer = await CustomerDAO.find_one_or_none(id=customer_id)
    if not find_customer:
        raise CannotFindCustomer
    return await BookTransactionDAO.find_all(customer_id=customer_id, returned_date=None)


@router.get("/last-visit/{customer_id}")
async def get_last_visit_date_func(customer_id: int):
    """Получение даты, последнего посещения библиотеки читателем"""
    find_customer = await CustomerDAO.find_one_or_none(id=customer_id)
    if not find_customer:
        raise CannotFindCustomer
    result = await CustomerDAO.get_last_visit_date(customer_id)
    if result:
        return result.transaction_date


@router.get("/mvp-genre/{customer_id}")
async def get_mvp_genre_by_customer(customer_id: int):
    """Получение любимого жанра по ID читателя"""
    find_customer = await CustomerDAO.find_one_or_none(id=customer_id)
    if not find_customer:
        raise CannotFindCustomer
    result = await BookTransactionDAO.find_all(customer_id=customer_id)
    book_count = {}
    for i in range(len(result)):
        find_book = await BookDAO.find_one_or_none(id=result[i].book_id)
        book_count[result[i].book_id] = find_book.genre_id
    count_dict = Counter(book_count.values())
    max_repeats = max(count_dict.values())
    most_frequent_values = [key for key, value in count_dict.items() if value == max_repeats]
    if most_frequent_values:
        return await GenreDAO.find_one_or_none(id=most_frequent_values[0])
