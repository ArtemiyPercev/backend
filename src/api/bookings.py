from fastapi import APIRouter, Body, HTTPException
from src.api.dependencies import DBdep, UserIdDep
from src.schemas.bookings import Booking, BookingAdd, BookingAddRequest


router = APIRouter(prefix="/hotels", tags=["Bookings"])


@router.get("/bookings")
async def get_all_bookings(
    db: DBdep,
):
    return await db.bookings.get_all()

@router.get("/bookings/me")
async def get_my_bookings(
    db: DBdep,
    user_id: UserIdDep,
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("/bookings")
async def add_booking(
        data_booking: BookingAddRequest,
        db: DBdep,
        user_id: UserIdDep,
):
    
    room_data = await db.rooms.get_one_or_none(id = data_booking.room_id)

    if room_data is None:
        raise HTTPException(status_code=404, detail="Room not found")


    _booking_data = BookingAdd(
        user_id=user_id,        
        price = room_data.price,
        **data_booking.model_dump()
    )

    result = await db.bookings.add(_booking_data)
    await db.commit()

    booking = Booking.model_validate(result, from_attributes=True)

    return {"Status": "OK", "data": booking}

    

