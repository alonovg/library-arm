INSERT INTO authors (author_full_name) VALUES
    ('Энди Вейр'), ('Агата Кристи'), ('Карлос Руис Сафон'), ('Джейн Остин'), ('Мольер'),
    ('Эрих Мария Ремарк'), ('Фридрих Ницше'), ('Марк Аврелий'),('Эрик Берне');

INSERT INTO genres (genre_name) VALUES
    ('Фантастика'), ('Детектив'), ('Роман'),
    ('Комедия'), ('Философия'),('Психология');

INSERT INTO books (title, author_id, availability, genre_id) VALUES
    ('Марсианин', 1, 1, 1), ('Убийство в Восточном экспрессе', 2, 1, 2),
    ('Тень ветра', 3, 1, 2), ('Гордость и предубеждение', 4, 1, 3),
    ('Тартюф', 5, 1, 4), ('Три товарища', 6, 1, 4),
    ('Так говорил Заратустра', 7, 1, 5), ('Размышления', 8, 1, 5),
    ('Игры, в которые играют люди', 9, 1, 6), ('Воля к власти', 7, 1, 5),
    ('Экклесиа гоминис', 7, 1, 5), ('Сумерки идолов', 7, 1, 5),
    ('Ориент Экспресс', 2, 1, 2), ('Смерть на Ниле', 2, 1, 2),
    ('Загадка желтых ирисов', 2, 1, 2);

INSERT INTO customers (customer_full_name, date_of_birth, address, phone_number) VALUES
    ('Петров Петр Петрович', '1980-05-15', 'ул. Ленина, д. 20, кв. 3', '+79123456789'),
    ('Козлов Игорь Николаевич', '1988-12-03', 'ул. Советская, д. 5, кв. 12', '+79876543210'),
    ('Иванова Ольга Александровна', '1975-04-10', 'ул. Пушкина, д. 8, кв. 2', '+79998887766');

INSERT INTO transaction_types (type_name) VALUES
    ('Взял'), ('Вернул');