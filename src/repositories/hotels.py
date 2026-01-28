from datetime import date

from sqlalchemy import select

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
    ):
        """
        Получить отели, в которых есть хотя бы один свободный номер
        в указанный период даты.
        """

        # Подзапрос: id номеров, которые доступны в указанный период
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from,
            date_to=date_to,
        )

        # Подзапрос: id отелей, которым принадлежат эти номера
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        # Основной запрос по отелям
        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids_to_get))