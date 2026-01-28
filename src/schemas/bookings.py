from datetime import date, datetime
from pydantic import BaseModel, ConfigDict

class BookingAdd(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int


class Booking(BookingAdd):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date
