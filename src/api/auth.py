from fastapi import APIRouter

from passlib.context import CryptContext

from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from fastapi.exceptions import HTTPException


router = APIRouter(prefix="/auth", tags=["authorisation and authentication"])



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(
    data: UserRequestAdd
):
    async with async_session_maker() as session:
        existing_user = await UsersRepository(session).get_one_or_none(email=data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        hashed_password = pwd_context.hash(data.password)
        new_user_data = UserAdd(
            email=data.email,
            hashed_password=hashed_password,
            name=data.name,
            surname=data.surname,
            username=data.username,
        )
        user = await UsersRepository(session).add(new_user_data)    
        await session.commit()
    return user 