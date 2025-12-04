from pydantic import BaseModel, ConfigDict, Field, EmailStr 



class UserRequestAdd(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    surname: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8, max_length=100)

class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    name: str = Field(min_length=1, max_length=100)
    surname: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=1, max_length=100)

class User(UserAdd):
    id: int     
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    surname: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=1, max_length=100)

    model_config = ConfigDict(from_attributes=True)

