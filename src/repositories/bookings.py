from src.schemas.bookings import Booking
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from sqlalchemy import select

class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

