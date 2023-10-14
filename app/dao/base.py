from sqlalchemy import select, insert, delete, update

from app.database.db import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """SELECT * FROM table_name WHERE column1 = value1 AND column2 = value2 LIMIT 1;"""
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        """SELECT * FROM table_name WHERE column1 = value1 AND column2 = value2;"""
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        """
        INSERT INTO table_name (column1, column2, column3)
        VALUES (value1, value2, value3)
        RETURNING id;
        """
        query = insert(cls.model).values(**data).returning(cls.model.id)
        async with async_session_maker() as session:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()

    @classmethod
    async def delete(cls, **filter_by):
        """DELETE FROM table_name WHERE column1 = value1 AND column2 = value2;"""
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update(cls, data_id, values):
        """
        UPDATE table_name
        SET column1 = value1, column2 = value2
        WHERE id = data_id;
        """
        async with async_session_maker() as session:
            query = (update(cls.model)
                     .where(cls.model.id == data_id)
                     .values(**values)
                     )
            await session.execute(query)
            await session.commit()
