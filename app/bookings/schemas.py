from datetime import date
from pydantic import BaseModel


class SBookings(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int


class SBookingsShort(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date


class SExtendedBookings(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    total_cost: int
    total_days: int
    price: int
    name: str
    description: str
    services: list
    image_id: int
