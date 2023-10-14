import pytest

from app.books.dao import BookDAO


@pytest.mark.parametrize("title, author_id, availability, genre_id", [
    ("Test book - First", 5, True, 3),
    ("Test book - Second", 2, False, 4),
])
async def test_add_and_get_book(title, author_id, availability, genre_id):
    new_book = await BookDAO.add(
        title=title,
        author_id=author_id,
        availability=availability,
        genre_id=genre_id,
    )
    find_book = await BookDAO.find_one_or_none(id=new_book.id)
    assert find_book is not None
    assert find_book.title == title
    assert find_book.author_id == author_id
    assert find_book.availability == availability
    assert find_book.genre_id == genre_id
