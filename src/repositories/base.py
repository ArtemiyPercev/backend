from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel


class BaseRepository():
    model: None
    def __init__(self, session):
        self.session = session

    async def get_all(self, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self,data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)
        return result.scalars().one()

    async def edit(self, data: BaseModel, **filter_by):
        update_stmt = update(self.model).values(**data.model_dump())
        for key, value in filter_by.items():
            update_stmt = update_stmt.where(getattr(self.model, key) == value)
        update_stmt = update_stmt.returning(self.model)
        result = await self.session.execute(update_stmt)
        return result.scalars().one()
       


    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model)
        for key, value in filter_by.items():
            delete_stmt = delete_stmt.where(getattr(self.model, key) == value)
        await self.session.execute(delete_stmt)

