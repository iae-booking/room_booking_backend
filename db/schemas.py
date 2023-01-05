from pydantic import BaseModel, EmailStr
from typing import Union, List, Optional
from datetime import date
from typing import List

class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True


class CreditCard(OrmBaseModel):
    safety_number: str
    card_id: str
    expire_date: date

class MemberInfo(OrmBaseModel):
    email: EmailStr
    name: str
    gender: int
    phone: Union[str, None] = None
    images: Union[List[bytes], None] = None

class Member(MemberInfo):
    password: str

class MemberCreditCardAndMemberType(MemberInfo):
    credit_cards: List[CreditCard]
    member_type: int

class MemberType(OrmBaseModel):
    member_type: int = 0

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
    images: Union[List[bytes], None] = None

class HotelForGetUpdate(Hotel):
    id: Union[int, None] = None


class CreateRoom(OrmBaseModel):
    room_name: str
    quantity: Union[int, None] = None
    bed_type: Union[str, None]
    capacity: int
    introduction: Union[str, None]
    installation: Union[str, None]
    original_price: int
    price: int
    hotel_id : int


class GetAndUpdateRoom(OrmBaseModel):
    id: int
    room_name: str
    quantity: Union[int, None] = None
    bed_type: Union[str, None]
    capacity: int
    introduction: Union[str, None]
    installation: Union[str, None]
    original_price: int
    price: int


class Rate(OrmBaseModel):
    evaluation: int
    comments: Union[str, None] = None
    images: Union[List[bytes], None] = None
    order_id: int


class RequestResult(OrmBaseModel):
    status: str


class ResponseRequestWithObjectId(RequestResult):
    id: int
