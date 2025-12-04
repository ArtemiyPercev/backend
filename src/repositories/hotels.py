from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from sqlalchemy import select, func
from src.schemas.hotels import Hotel

class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
        self,
        location,
        title, 
        per_page,
        offset,
    ) -> list[Hotel]:
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
      return [Hotel.model_validate(model, from_attributes=True) for model in result.scalars().all()]




