from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [column.name for column in Bookings.__table__.columns] + [Bookings.user, Bookings.rooms]
    name = "Бронирование"
    name_plural = "Бронирования"
    icon = "fa-solid fa-book"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [column.name for column in Hotels.__table__.columns] + [Hotels.rooms]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [column.name for column in Rooms.__table__.columns] + [Rooms.hotel, Rooms.booking]
    name = "Номер"
    name_plural = "Номера"
    icon = "fa-solid fa-bed"
