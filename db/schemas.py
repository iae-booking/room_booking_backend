from pydantic import BaseModel, EmailStr
from typing import Union, List
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

class MemberInfo(OrmBaseModel):
    email: EmailStr
    name: str
    gender: int
    phone: Union[str, None] = None

class MemberCreditCard(MemberInfo):
    credit_cards: List[CreditCard]

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

class Room(OrmBaseModel):
    room_name: Union[str, None]
    quantity: Union[int, None]
    capacity: Union[int, None]
    bed_type: Union[str, None] = None
    introduction: Union[str, None] = None
    installation: Union[str, None] = None
    original_price: Union[int, None]
    iae_price: Union[int, None]
    hotel_id: Union[int, None]

class Order(OrmBaseModel):
    fee: Union[int, None]
    amount: Union[int, None]
    payment_method: Union[int, None]
    end_date: Union[str, None]
    start_date: Union[str, None]
    room_id: Union[int, None]

class Rate(OrmBaseModel):
    evaluation: int
    comments: Union[str, None] = None
    images: Union[str, List[bytes], None] = None
    order_id: int


class RequestResult(OrmBaseModel):
    status: str

