from fastapi import Query, Body, APIRouter
from src.api.dependencies import PaginationParams, PaginationDep
from src.schemas.hotels import Hotel, HotelPatch

from sqlalchemy import insert, select
from src.models.hotels import HotelsOrm
from src.database import async_session_maker, engine



router = APIRouter(prefix="/hotels", tags=["Hotels"])




@router.get("/")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="The title of the hotel"),
    location: str | None = Query(None, description="The place of the hotel"),
):
    per_page = pagination.per_page or 5

    async with async_session_maker() as session:
        query = select(HotelsOrm)

        if title:
            query = query.where(HotelsOrm.title.ilike(f"%{title}%"))
        if location:
            query = query.where(HotelsOrm.location.ilike(f"%{location}%"))

        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )

        result = await session.execute(query)
        hotels = result.scalars().all()

        return hotels




        
        

    # if pagination.page and pagination.per_page:
    #     return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
    


# @app.get("/hotels")
# def get_all_hotels():
#     return hotels

@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
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
        add_hotel_stmt =  insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine ,compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}")
def change_hotel(
    hotel_id: int,
    hotel_data: Hotel
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name

    return {"Status: OK"}


@router.patch("/{hotel_id}", summary="Поменять одну деталь", description="Обязательно документацию ")
def change_one_thing(
    hotel_id: int,
    hotel_data: HotelPatch

):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title is not None and hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name is not None and hotel_data.name:
        hotel["name"] = hotel_data.name

    return {"Status: OK"}