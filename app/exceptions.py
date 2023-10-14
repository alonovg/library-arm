from fastapi import HTTPException, status


class LibraryException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(LibraryException):
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"


class CannotAddDataToDatabase(LibraryException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


class IncorrectEmailOrPasswordException(LibraryException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверная почта или пароль"


class UserIsNotPresentException(LibraryException):
    status_code=status.HTTP_401_UNAUTHORIZED


class TokenExpiredException(LibraryException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Срок действия токена истек"


class TokenAbsentException(LibraryException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"


class IncorrectTokenFormatException(LibraryException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный формат токена"


class CannotFindBook(LibraryException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Книга не была найдена"


class BookAlreadyBusyException(LibraryException):
    status_code=status.HTTP_409_CONFLICT
    detail="Книгу уже взяли"


class CannotFindAuthor(LibraryException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Автор не был найден"


class AuthorAlreadyExistException(LibraryException):
    status_code=status.HTTP_409_CONFLICT
    detail="Автор уже существует"


class CannotFindBookTransaction(LibraryException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Транзакция по книге не была найдена"


class CannotFindGenre(LibraryException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Жанр не был найден"


class GenreAlreadyExistException(LibraryException):
    status_code=status.HTTP_409_CONFLICT
    detail="Жанр уже существует"


class CannotFindCustomer(LibraryException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не был найден"


class CannotFindTransactionType(LibraryException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Тип транзакции не был найден"
