from datetime import date

from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRooms
from app.hotels.schemas import SHotelsWithRoomsLeft


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_hotels(cls, location: str, date_from: date, date_to: date) -> list[SHotelsWithRoomsLeft | None]:
        hotels = await cls.find_like('location', location)

        hotels_with_free_rooms: list[SHotelsWithRoomsLeft | None] = []

        for hotel in hotels:
            rooms: list[SRooms] = await RoomDAO.find_all(hotel_id=hotel.id)

            quantity = 0
            for room in rooms:
                quantity += await RoomDAO.get_rooms_left(room.id, date_from, date_to)

            if quantity > 0:
                hotel_dict = dict(hotel)
                hotel_dict["rooms_left"] = quantity
                hotel_with_rooms_left = SHotelsWithRoomsLeft(**hotel_dict)
                hotels_with_free_rooms.append(hotel_with_rooms_left)

        return hotels_with_free_rooms

