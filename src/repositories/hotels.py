from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from sqlalchemy import select, func


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
        self,
        location,
        title, 
        per_page,
        offset,
    ):
      query = select(HotelsOrm)

      if title:
          query = query.where(HotelsOrm.title.ilike(f"%{title}%"))
      if location:
          query = query.where(HotelsOrm.location.ilike(f"%{location}%"))

      query = (
          query
          .limit(per_page)
          .offset(offset)
      )

      result = await self.session.execute(query)
      return result.scalars().all()



