import pytest

from app.bookings.dao import BookingDAO
from datetime import datetime


@pytest.mark.parametrize(
    "user_id,room_id",
    [
        (2, 2),
        (2, 3),
        (1, 4),
        (1, 4),
    ],
)
async def test_booking_crud(user_id, room_id):
    new_booking = await BookingDAO().add(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.strptime("2024-01-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2024-01-23", "%Y-%m-%d"),
    )

    assert new_booking.user_id == user_id
    assert new_booking.room_id == room_id

    new_booking = await BookingDAO.find_one_or_none(id=new_booking.id)

    assert new_booking is not None

    await BookingDAO.delete(model_id=new_booking.id, user_id=user_id)

    deleted_booking = await BookingDAO.find_one_or_none(id=new_booking.id)
    assert deleted_booking is None
