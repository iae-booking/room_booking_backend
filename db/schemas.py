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
    room_name: str
    quantity: int
    capacity: int
    bed_type: Union[str, None] = None
    introduction: Union[str, None] = None
    installation: Union[str, None] = None
    Original_price: int
    IAE_price:int

class Order(OrmBaseModel):
    fee: int
    amount: int
    payment_method: int
    end_data: str
    start_data: str

class Rate(OrmBaseModel):
    evaluation: int
    comments: Union[str, None] = None
    images: Union[str, List[bytes], None] = None
    order_id: int


class RequestResult(OrmBaseModel):
    status: str

