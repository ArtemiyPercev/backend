from fastapi import Query, Body, APIRouter
from sqlalchemy.ext.asyncio import async_session
from src.api.dependencies import PaginationParams, PaginationDep
from src.schemas.hotels import Hotel, HotelPatch


from src.database import async_session_maker, engine
from src.repositories.hotels import HotelsRepository


router = APIRouter(prefix="/hotels", tags=["Hotels"])




@router.get("/")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="The title of the hotel"),
    location: str | None = Query(None, description="The place of the hotel"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            per_page=per_page,
            offset=per_page * (pagination.page - 1)
        )

    return hotels


@router.get("/hotel_id")
async def get_hotel(
    hotel_id:int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)




@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"} 

@router.post("/")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 звезд у моря",
            "location": "Sochi, ul moria. 19",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Дубай У фонтана",
            "location": "Dubai, ul dubai. 12",
        }
    }
})
):

    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def change_hotel(
    hotel_id: int,
    hotel_data: Hotel
):

    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Поменять одну деталь", description="Обязательно документацию ")
async def change_one_thing(
    hotel_id: int,
    hotel_data: HotelPatch

):

    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id, exclude_unset=True)
        await session.commit()

    return {"Status: OK"}