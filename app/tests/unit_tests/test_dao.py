import pytest

from app.books.dao import BookDAO


@pytest.mark.parametrize("book_id, title, exists", [
    (1, "Марсианин", True),
    (20, "Test", False)
])
async def test_find_book_one_or_none(book_id, title, exists):
    book = await BookDAO.find_one_or_none(id=book_id)
    if exists:
        assert book
        assert book.id == book_id
        assert book.title == title
    else:
        assert not book
