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
    image_path: Union[List[bytes], None] = None

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
    images: Union[str, List[bytes], None] = None


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
    images: Union[str, List[bytes], None] = None


class Rate(OrmBaseModel):
    evaluation: int
    comments: Union[str, None] = None
    images: Union[str, List[bytes], None] = None
    order_id: int


class RequestResult(OrmBaseModel):
    status: str


class Search(OrmBaseModel):
    place: str
    number_of_people: int
    start_date: date
    end_date: date
class Order(OrmBaseModel):
    room_id: int
    start_date: date
    end_date: date