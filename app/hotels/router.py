import asyncio
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotels, SHotelsWithRoomsLeft

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.get("/{location}")
@cache(expire=30)
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(
        ..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"
    ),
) -> list[SHotelsWithRoomsLeft | None]:
    await HotelDAO.check_date(date_from, date_to)

    return await HotelDAO.get_hotels(location, date_from, date_to)


@router.get("{id/{hotel_id}")
async def get_hotel(hotel_id: int) -> SHotels | None:
    return await HotelDAO.find_by_id(hotel_id)
