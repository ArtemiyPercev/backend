from nt import error
from fastapi import FastAPI, Query, Body
import uvicorn


app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "Sochi Hotel"},
    {"id": 2, "title": "Dubai", "name": "Dubai Hotel"},
    {"id": 3, "title": "Moscow", "name": "Moscow Hotel"},
]

@app.get("/")
def get_hotels(
    id: int | None = Query(None, description="The id of the hotel"),
    title: str | None = Query(None, description="The title of the hotel")
    ):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_

# @app.get("/hotels")
# def get_all_hotels():
#     return hotels

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@app.post("/hotels")
def create_hotel(
    title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}



@app.put("/hotels/{hotel_id}")
def change_hotel(
    hotel_id: int , 
    title: str = Body(),
    name: str= Body()
):
    global hotels 
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            break
    else:
        return {"Error: 404"}


    return {"hotel_id": hotel_id, "title": title, "name": name}


@app.patch("/hotels/{hotel_id}")
def change_one_detail(
    hotel_id: int,
    title: None | str = Body(),
    name: None | str = Body()
):

    global hotels 
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None and hotel["title"] != title:
                hotel["title"] = title
            if name is not None and hotel["name"] != name:
                hotel["name"] = name
            break

    else: 
        return {"Error: 404"}
    
    return {"hotel_id": hotel_id, "title": title, "name": name}

                



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)