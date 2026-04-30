from pydantic import BaseModel, validator
from typing import Optional


class SearchRequest(BaseModel):
    keyword: str

    @validator("keyword")
    def keyword_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("keyword ต้องไม่ว่างเปล่า")
        return v.strip()


class SearchResponse(BaseModel):
    id: int
    building: str
    floor: int
    type: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    crowd: str


class RestroomCreate(BaseModel):
    """Schema สำหรับสร้างห้องน้ำใหม่"""
    building: str
    floor: int
    type: str
    latitude: float
    longitude: float
    crowd_level: str = "low"

    @validator("building")
    def building_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("ชื่ออาคารต้องไม่ว่างเปล่า")
        return v.strip()

    @validator("floor")
    def floor_must_be_positive(cls, v):
        if v < 1:
            raise ValueError("ชั้นต้องมากกว่า 0")
        return v

    @validator("type")
    def type_must_be_valid(cls, v):
        valid_types = ["male", "female", "disabled"]
        if v.lower() not in valid_types:
            raise ValueError(f"ประเภทต้องเป็น {', '.join(valid_types)}")
        return v.lower()


class RestroomResponse(BaseModel):
    """Schema สำหรับการตอบสนองห้องน้ำ"""
    id: int
    building: str
    floor: int
    type: str
    latitude: float
    longitude: float
    crowd_level: str

    class Config:
        from_attributes = True
