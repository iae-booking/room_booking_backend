from pydantic import BaseModel, EmailStr
from typing import Union, List
from datetime import date
from typing import List

class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True

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

class RequestResult(OrmBaseModel):
    status: str

