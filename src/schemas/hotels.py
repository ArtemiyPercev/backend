from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str
    location: str 

class HotelPatch(BaseModel):
    title: None | str = None
    location: None | str = None