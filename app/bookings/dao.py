from datetime import date

from sqlalchemy import select, and_, insert, delete

from app.bookings.models import Bookings
from app.bookings.schemas import SBookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import BookingIsNotPresentException
from app.hotels.rooms.models import Rooms
from app.hotels.rooms.dao import RoomDAO


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date,
    ):
        async with async_session_maker() as session:
            rooms_left: int = await RoomDAO.get_rooms_left(room_id, date_from, date_to)

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()

                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Bookings)

                await session.execute(add_booking)
                await session.commit()
                return dict(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price)
            else:
                return None

    @classmethod
    async def get_external_bookings(cls, **filter_by):
        async with async_session_maker() as session:
            extended_bookings = select(Bookings.room_id, Bookings.user_id,
                                       Bookings.date_from, Bookings.date_to,
                                       Bookings.total_cost, Bookings.total_days,
                                       Rooms.price, Rooms.image_id,
                                       Rooms.name, Rooms.description,
                                       Rooms.services,
                                       ).join(Rooms, Bookings.room_id == Rooms.id).cte("extended_bookings")

            get_extended_bookings_for_user = select(extended_bookings).filter_by(**filter_by)

            result = await session.execute(get_extended_bookings_for_user)
            return result.mappings().all()

    @classmethod
    async def delete(cls, model_id: int, user_id: int):
        async with async_session_maker() as session:
            booking_for_delete = await cls.find_one_or_none(id=model_id,
                                                            user_id=user_id)

            if not booking_for_delete:
                raise BookingIsNotPresentException

            query = delete(Bookings).where(and_(Bookings.id == model_id,
                                                Bookings.user_id == user_id))
            await session.execute(query)
            await session.commit()
