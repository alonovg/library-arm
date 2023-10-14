from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.authors.router import get_authors, get_mvp_author
from app.book_transactions.router import get_transactions_joined
from app.books.router import get_mvp_book, get_books_joined
from app.customers.router import get_customers, get_last_visit_date_func, get_mvp_genre_by_customer, \
    get_count_book_all_time, get_count_book_at_the_moment
from app.genres.router import get_genres, get_mvp_genre


router = APIRouter(
    prefix="/ui",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates/")


@router.get("")
async def get_main_page(
        request: Request,
        customers=Depends(get_customers),
        books=Depends(get_books_joined),
        authors=Depends(get_authors),
        genres=Depends(get_genres),
        book_transactions=Depends(get_transactions_joined),
        mvp_book=Depends(get_mvp_book),
        mvp_author=Depends(get_mvp_author),
        mvp_genres=Depends(get_mvp_genre)
):
    customer_count = {}
    last_visit = {}
    customer_books_atm = {}
    customer_mvp_genres = {}
    for customer in customers:
        customer_count[customer.id] = len(await get_count_book_all_time(customer.id))
        customer_books_atm[customer.id] = len(await get_count_book_at_the_moment(customer.id))
        last_visit[customer.id] = await get_last_visit_date_func(customer.id)
        customer_mvp_genres[customer.id] = await get_mvp_genre_by_customer(customer.id)
    return templates.TemplateResponse(name="index.html",
                                      context={
                                          "request": request,
                                          "customers": customers,
                                          "books": books,
                                          "authors": authors,
                                          "genres": genres,
                                          "book_transactions": book_transactions,
                                          "customers_count": len(customers),
                                          "books_count": len(books),
                                          "customer_count": customer_count,
                                          "last_visit": last_visit,
                                          "mvp_book": mvp_book,
                                          "mvp_author": mvp_author,
                                          "mvp_genres": mvp_genres,
                                          "customer_books_atm": customer_books_atm,
                                          "customer_mvp_genres": customer_mvp_genres
                                      })
