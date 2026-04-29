from pydantic import BaseModel, validator
from typing import Optional


class SearchRequest(BaseModel):
    keyword: str

    @validator("keyword")
    def keyword_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("keyword ต้องไม่ว่างเปล่า")
        return v.strip()


class RestroomCreate(BaseModel):
    building: str
    floor: int
    type: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    crowd_level: Optional[str] = "low"

    @validator("building", "type")
    def field_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("field ต้องไม่ว่างเปล่า")
        return v.strip()


class RestroomResponse(BaseModel):
    id: int
    building: str
    floor: int
    type: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    crowd_level: str

    class Config:
        orm_mode = True


class SearchResponse(BaseModel):
    id: int
    building: str
    floor: int
    type: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    crowd: str
