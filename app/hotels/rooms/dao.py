from datetime import date

from sqlalchemy import and_, func, or_, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.hotels.rooms.schemas import SExtendedRooms


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_rooms_left(cls, room_id: int, date_from: date, date_to: date) -> int:
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
            (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to,
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from,
                            ),
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            get_rooms_left = (
                select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                        "rooms_left"
                    )
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            rooms_left = await session.execute(get_rooms_left)
            return rooms_left.scalar()

    @classmethod
    async def get_extended_rooms(
        cls, hotel_id: int, date_from: date, date_to: date
    ) -> list[SExtendedRooms | None]:
        rooms = await cls.find_all(hotel_id=hotel_id)

        result_rooms: list[SExtendedRooms | None] = []
        for room in rooms:
            rooms_left = await cls.get_rooms_left(room.id, date_from, date_to)
            total_cost = (date_to - date_from).days * room.price

            dict_room = dict(room)
            dict_room["rooms_left"] = rooms_left
            dict_room["total_cost"] = total_cost
            room_with_cost_and_rooms_left = SExtendedRooms(**dict_room)
            result_rooms.append(room_with_cost_and_rooms_left)

        return result_rooms
