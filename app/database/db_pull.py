import psycopg2

from app.database.table_sql import table_definitions
from app.database.data_sql import data_definitions

DB_NAME = 'library_db'
TEST_DB_NAME = 'test_library_db'


def db_connection(database):
    def decorator(func):
        def wrapper(*args, **kwargs):
            conn = psycopg2.connect(
                database=database,
                user='postgres',
                password='postgres',
                host='127.0.0.1',
                port='5432'
            )
            conn.autocommit = True
            result = func(conn, *args, **kwargs)
            conn.close()
            return result
        return wrapper
    return decorator


@db_connection(database=f"{DB_NAME}")
def pull(conn, sql_list: dict):
    with conn.cursor() as cursor:
        for data_definition, data_name in sql_list:
            cursor.execute(data_definition)
            print(f"{data_name} - ОК")


@db_connection(database="postgres")
def create_db(conn, db_name):
    with conn.cursor() as cursor:
        cursor.execute(f"""SELECT 1 FROM pg_database WHERE datname = '{db_name}';""")
        exists = cursor.fetchone()
        if exists:
            print(f"База данных с именем '{db_name}' существует")
        else:
            sql_query = f'''CREATE DATABASE {db_name}'''
            cursor.execute(sql_query)
            print(f"База данных создана '{db_name}'")


@db_connection(database="postgres")
def db_del(conn, db_name):
    with conn.cursor() as cursor:
        sql_query = f"""DROP DATABASE {db_name};"""
        cursor.execute(sql_query)
        print(f"База данных '{db_name}' удалена")


def main():
    while True:
        answer = input(f"""
            Please select:
            1. CREATE DB
            2. CREATE TEST DB
            3. Create table in DB: {DB_NAME}
            4. Insert data in DB: {DB_NAME}
            5. DELETE DB
            6. DELETE TEST DB
            For exit type any char and press enter....
    
        """)
        if answer == "1":
            create_db(db_name=DB_NAME)
        elif answer == "2":
            create_db(db_name=TEST_DB_NAME)
        elif answer == "3":
            pull(table_definitions)
        elif answer == "4":
            pull(data_definitions)
        elif answer == "5":
            db_del()
        else:
            break


if __name__ == '__main__':
    main()
