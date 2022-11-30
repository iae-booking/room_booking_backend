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

class member(Base):
    __tablename__ = "member"
    # todo fill in the rest of this table
    member_id = Column(Integer, primary_key=True)
