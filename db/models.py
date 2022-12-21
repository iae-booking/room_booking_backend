from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Sequence

from .database import Base


class Hotel(Base):
    __tablename__ = "hotel"

    id = Column(Integer, Sequence('hotel_id_seq'), primary_key=True)
    member_id = Column(Integer)
    hotel_name = Column(String)
    regulation = Column(String)
    city = Column(String)
    region = Column(String)
    road_and_number = Column(String)
    certificate_number = Column(String)
    image_path = Column(String)
    member_id = Column(Integer, ForeignKey("member.member_id"))

class Room(Base):
    __tablename__ = "room"

    id = Column(Integer, Sequence('room_id_seq'), primary_key=True)
    room_name = Column(String)
    quantity = Column(Integer)
    capacity = Column(Integer)
    bed_type= Column(String)
    introduction= Column(String)
    installation= Column(String)
    original_price= Column(Integer)
    iae_price= Column(Integer)
    hotel_id = Column(Integer)
    hotel_id = Column(Integer, ForeignKey("hotel.id"))