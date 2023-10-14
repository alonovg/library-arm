from sqladmin import ModelView

from app.authors.models import Authors
from app.book_transactions.models import BookTransactions
from app.books.models import Books
from app.customers.models import Customers
from app.genres.models import Genres
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    can_edit = False
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"


class CustomersAdmin(ModelView, model=Customers):
    column_list = [c.name for c in Customers.__table__.c] + [Customers.book_transaction]
    name = "Customer"
    name_plural = "Customers"
    icon = "fa-solid fa-users"


class AuthorsAdmin(ModelView, model=Authors):
    column_list = [c.name for c in Authors.__table__.c] + [Authors.book]
    name = "Author"
    name_plural = "Authors"
    icon = "fa-solid fa-pencil"


class GenresAdmin(ModelView, model=Genres):
    column_list = [c.name for c in Genres.__table__.c] + [Genres.book]
    name = "Genre"
    name_plural = "Genres"
    icon = "fa fa-window-maximize"


class BooksAdmin(ModelView, model=Books):
    column_list = [c.name for c in Books.__table__.c] + [Books.author] + [Books.genre] + [Books.book_transaction]
    name = "Book"
    name_plural = "Books"
    icon = "fa fa-book"


class BookTransactionsAdmin(ModelView, model=BookTransactions):
    column_list = [c.name for c in BookTransactions.__table__.c] + [BookTransactions.book] + [BookTransactions.customer]
    name = "Book Transaction"
    name_plural = "Book Transactions"
    icon = "fa fa-bars"
