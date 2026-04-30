from pydantic import BaseModel
from typing import Optional


class RestroomBase(BaseModel):
    building: str
    floor: int
    type: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    crowd_level: str


class RestroomCreate(RestroomBase):
    pass


class RestroomUpdate(RestroomBase):
    building: Optional[str] = None
    floor: Optional[int] = None
    type: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    crowd_level: Optional[str] = None


class RestroomResponse(RestroomBase):
    id: int

    class Config:
        from_attributes = True