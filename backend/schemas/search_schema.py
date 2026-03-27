from pydantic import BaseModel

class SearchRequest(BaseModel):
    keyword: str

class SearchResponse(BaseModel):
    building: str
    floor: int
    type: str
    crowd: str