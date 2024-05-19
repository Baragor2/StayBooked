from datetime import date, timedelta, datetime

from fastapi import APIRouter, Depends, status, Query
from pydantic import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SExtendedBookings, SBookingsShort
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix="/bookings",
    tags=['Bookings'],
)


@router.get("")
async def get_bookings_with_rooms(user: Users = Depends(get_current_user)) -> list[SExtendedBookings]:
    return await BookingDAO.get_external_bookings(user_id=user.id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_booking(
        room_id: int,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
        user: Users = Depends(get_current_user),
):
    await BookingDAO.check_date(date_from, date_to)

    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)

    booking = parse_obj_as(SBookingsShort, booking).dict()

    send_booking_confirmation_email.delay(booking, user.email)
    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingDAO.delete(booking_id, user.id)
