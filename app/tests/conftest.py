import asyncio

import pytest
from httpx import AsyncClient

import json
from datetime import datetime

from sqlalchemy import insert

from app.config import settings
from app.authors.models import Authors
from app.book_transactions.models import BookTransactions
from app.books.models import Books
from app.customers.models import Customers
from app.database.db import engine, Base, async_session_maker
from app.genres.models import Genres
from app.users.models import Users
from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database_test():
    assert settings.MODE == "TEST"
    async with engine.begin() as conn:
        # Удаление всех заданных нами таблиц из БД
        await conn.run_sync(Base.metadata.drop_all)
        # Добавление всех заданных нами таблиц из БД
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/administration/mock_files/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    authors = open_mock_json("authors")
    genres = open_mock_json("genres")
    books = open_mock_json("books")
    customers = open_mock_json("customers")
    users = open_mock_json("users")
    book_transactions = open_mock_json("book_transactions")

    for book_transaction in book_transactions:
        # # SQLAlchemy не принимает дату в текстовом формате, поэтому форматируем к datetime
        book_transaction["transaction_date"] = datetime.strptime(book_transaction["transaction_date"], "%Y-%m-%d")
        book_transaction["expected_return_date"] = datetime.strptime(
            book_transaction["expected_return_date"], "%Y-%m-%d")
        if book_transaction["returned_date"]:
            book_transaction["returned_date"] = datetime.strptime(book_transaction["returned_date"], "%Y-%m-%d")

    for customer in customers:
        customer["date_of_birth"] = datetime.strptime(customer["date_of_birth"], "%Y-%m-%d")

    async with async_session_maker() as session:
        for Model, values in [
            (Authors, authors),
            (Genres, genres),
            (Books, books),
            (Customers, customers),
            (Users, users),
            (BookTransactions, book_transactions),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)
        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    "Асинхронный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    "Асинхронный аутентифицированный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/auth/login", json={
            "email": "admin@admin.net",
            "password": "admin",
        })
        assert ac.cookies["library_access_token"]
        yield ac
