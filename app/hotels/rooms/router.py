from datetime import date, datetime

from fastapi import Query

from app.hotels.rooms.schemas import SExtendedRooms
from app.hotels.router import router
from app.hotels.rooms.dao import RoomDAO


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_hotel_and_data(
        hotel_id: int,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {datetime.now().date()}"),
) -> list[SExtendedRooms | None]:
    return await RoomDAO.get_extended_rooms(hotel_id, date_from, date_to)

