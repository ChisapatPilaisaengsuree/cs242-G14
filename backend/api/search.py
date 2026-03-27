from fastapi import APIRouter
from schemas.search_schema import SearchRequest
from services.search_service import search_restrooms

router = APIRouter()

@router.post("/search")
def search(data: SearchRequest):
    result = search_restrooms(data.keyword)
    return result