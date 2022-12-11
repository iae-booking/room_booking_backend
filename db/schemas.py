from pydantic import BaseModel, EmailStr
# from pydantic.types import PaymentCardNumber
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
    # credit_cards: PaymentCardNumber

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
        
class Room(OrmBaseModel):
    room_name: str
    quantity: Union[str, None] = None
    capacity: int
    price: int

class Order(OrmBaseModel):
    fee: int
    amount: int
    payment_method: int
    end_data: str
    start_data: str

class Rate(OrmBaseModel):
    evaluation: str
    comments: Union[str, None] = None
    image_path: Union[str, None] = None
    order_id: int


class RequestResult(OrmBaseModel):
    status: str

