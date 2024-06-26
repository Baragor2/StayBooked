from pydantic import BaseModel


class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list
    quantity: int
    image_id: int


class SExtendedRooms(SRooms):
    rooms_left: int
    total_cost: int
