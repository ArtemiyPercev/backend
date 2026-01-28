from datetime import date
from typing import Annotated

from fastapi import Query, Body, APIRouter
from src.api.dependencies import DBdep, PaginationDep
from src.schemas.hotels import Hotel, HotelPatch, HotelAdd


router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/")
async def get_hotels(
    pagination: PaginationDep,
    db: DBdep,
    title: str | None = Query(None, description="The title of the hotel"),
    location: str | None = Query(None, description="The place of the hotel"),
    date_from: Annotated[date, Query(example="2026-01-15")] = ...,
    date_to: Annotated[date, Query(example="2026-01-16")] = ...,
):
    per_page = pagination.per_page or 5

    # Если нужно вернуться к простому get_all с пагинацией и фильтрами по названию/локации,
    # можно раскомментировать код ниже и доработать репозиторий.
    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     per_page=per_page,
    #     offset=per_page * (pagination.page - 1),
    # )

    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/hotel_id")
async def get_hotel(
    db: DBdep,
    hotel_id:int):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBdep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"} 

@router.post("/")
async def create_hotel(db: DBdep, hotel_data: HotelAdd = Body(openapi_examples={
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


        hotel = await db.hotels.add(hotel_data)
        await db.commit()
        return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def change_hotel(
    db: DBdep,
    hotel_id: int,
    hotel_data: Hotel
):

    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Поменять одну деталь", description="Обязательно документацию ")
async def change_one_thing(
    db: DBdep,
    hotel_id: int,
    hotel_data: HotelPatch

):

    await db.hotels.edit(hotel_data, id=hotel_id, exclude_unset=True)
    await db.commit()
    return {"Status: OK"}