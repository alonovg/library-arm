table_definitions = [(
    """
    CREATE TABLE IF NOT EXISTS authors (
        id SERIAL PRIMARY KEY,
        author_full_name VARCHAR NOT NULL);""", "authors_table"),
    ("""
    CREATE TABLE IF NOT EXISTS genres (
        id SERIAL PRIMARY KEY,
        genre_name VARCHAR NOT NULL);""", "genres_table"),
    ("""
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title VARCHAR NOT NULL,
        author_id INTEGER REFERENCES authors(id),
        availability BOOLEAN NOT NULL,
        genre_id INTEGER REFERENCES genres(id));""", "books_table"),
    ("""
    CREATE TABLE IF NOT EXISTS customers (
        id SERIAL PRIMARY KEY,
        customer_full_name VARCHAR NOT NULL,
        date_of_birth DATE NOT NULL,
        address VARCHAR NOT NULL,
        phone_number VARCHAR NOT NULL);""", "customers_table"),
    ("""
    CREATE TABLE IF NOT EXISTS book_transactions (
        id SERIAL PRIMARY KEY,
        book_id INTEGER REFERENCES books(id),
        customer_id INTEGER REFERENCES customers(id),
        transaction_date DATE NOT NULL,
        expected_return_date DATE NOT NULL,
        returned_date DATE);""", "book_transactions_table"),
    ("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR NOT NULL,
        hashed_password VARCHAR NOT NULL);""", "users_table")
]
