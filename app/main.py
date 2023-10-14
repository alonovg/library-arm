from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from sqladmin import Admin, ModelView
from starlette.applications import Starlette

from app.admin.auth import authentication_backend
from app.admin.views import UsersAdmin, CustomersAdmin, AuthorsAdmin, GenresAdmin, BooksAdmin, BookTransactionsAdmin
from app.administration.router import router as router_admin
from app.database.db import engine
from app.users.models import Users
from app.users.router import router_users
from app.users.router import router_auth
from app.customers.router import router as router_customers
from app.authors.router import router as router_authors
from app.genres.router import router as router_genres
from app.books.router import router as router_books
from app.book_transactions.router import router as router_transaction
from app.pages.router import router as router_pages


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router_admin)
app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_customers)
app.include_router(router_authors)
app.include_router(router_genres)
app.include_router(router_books)
app.include_router(router_transaction)
app.include_router(router_pages)


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(CustomersAdmin)
admin.add_view(AuthorsAdmin)
admin.add_view(GenresAdmin)
admin.add_view(BooksAdmin)
admin.add_view(BookTransactionsAdmin)
