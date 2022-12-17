from pydantic import BaseModel, EmailStr
from typing import Union
from datetime import date
from typing import List

class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True


class CreditCard(OrmBaseModel):
    safety_number: str
    card_id: str
    expire_date: date

class Member(OrmBaseModel):
    email: EmailStr
    password: str
    name: str
    gender: int
    phone: Union[str, None] = None
    image: Union[str, bytes, None] = None

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
    regulation: Union[str, None] = None
    introduction: Union[str, None] = None
    transportation: Union[str, None] = None
    attraction: Union[str, None] = None
    images: Union[str, List[bytes], None] = None

class Rate(OrmBaseModel):
    evaluation: int
    comments: Union[str, None] = None
    images: Union[str, List[bytes], None] = None
    order_id: int


class RequestResult(OrmBaseModel):
    status: str

