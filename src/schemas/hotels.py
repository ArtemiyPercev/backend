from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str
    name: str 

class HotelPatch(BaseModel):
    title: None | str = None
    name: None | str = None