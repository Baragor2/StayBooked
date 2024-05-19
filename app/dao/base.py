from datetime import date

from sqlalchemy import select, insert

from app.database import async_session_maker
from app.exceptions import (
    DateToLessThenDateFromException,
    BookingTimeIsMoreThanThirtyDaysException,
)


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(
                cls.model,
                cls.model.__table__.columns,
            ).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_like(cls, column: str, value: str):
        async with async_session_maker() as session:
            query = select(
                cls.model,
                cls.model.__table__.columns,
            ).where(getattr(cls.model, column).like(f"%{value}%"))
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data) -> None:
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def check_date(date_from: date, date_to: date):
        if date_to <= date_from:
            raise DateToLessThenDateFromException
        elif (date_to - date_from).days > 30:
            raise BookingTimeIsMoreThanThirtyDaysException
