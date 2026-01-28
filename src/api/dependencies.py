from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel
from typing import Annotated

from src.database import async_session_maker
from src.services.auth import AuthService
from utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="pages", ge=1)]
    per_page: Annotated[int | None, Query(None, description="per page hotels", ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="You forgot to provide access token")
    return access_token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_access_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]




async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBdep = Annotated[DBManager, Depends(get_db)]

