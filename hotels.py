from fastapi import FastAPI, Query, Body, APIRouter
from schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Hotels"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("/")
def get_hotels(
    id: int | None = Query(None, description="The id of the hotel"),
    title: str | None = Query(None, description="The title of the hotel"),
    page: int | None = Query(1, description="pages"),
    per_page: int | None = Query(3, description="per page hotels" )
    ):
    hotels_ = []
    for hotel in hotels[(page - 1) * per_page:page * per_page]:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_

# @app.get("/hotels")
# def get_all_hotels():
#     return hotels

@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@router.post("/")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 звезд у моря",
            "name": "sochi_u_morya",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Дубай У фонтана",
            "name": "dubai_fountain",
        }
    }
})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
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