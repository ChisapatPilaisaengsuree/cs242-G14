from sqlalchemy import Column, Integer, String, Float
from database.db import Base

class Restroom(Base):
    __tablename__ = "restrooms"

    id = Column(Integer, primary_key=True)
    building = Column(String)
    floor = Column(Integer)
    type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    crowd_level = Column(String)