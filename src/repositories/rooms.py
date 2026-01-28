from datetime import date

from sqlalchemy import select, func

from src.repositories.utils import rooms_ids_for_booking
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
        self,
        hotel_id: int | None,
        date_from: date,
        date_to: date,
    ):
        """
        Получить номера, доступные в указанный период.
        При переданном `hotel_id` выборка ограничивается конкретным отелем.
        """

        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from,
            date_to=date_to,
            hotel_id=hotel_id,
        )

        result = await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
        return result