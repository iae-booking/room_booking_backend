from pydantic import BaseModel, EmailStr
from typing import Union

class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True

class User(OrmBaseModel):
    email: EmailStr
    password: str
    name: str
    gender: int
    phone: Union[str, None] = None
    member_type: int

class Token(OrmBaseModel):
    access_token: str
    token_type: str

class TokenData(OrmBaseModel):
    username: Union[str, None] = None

class Hotel(OrmBaseModel):
    hotel_name: str
    city: Union[str, None] = None
    region: Union[str, None] = None
    road_and_number: Union[str, None] = None
