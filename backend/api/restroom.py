from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.services.search_service import calculate_distance
from backend.database.db import get_db
from backend.models.restroom import Restroom
from backend.schemas.search_schema import RestroomCreate, RestroomResponse

router = APIRouter()

@router.post("/restrooms", response_model=RestroomResponse, status_code=status.HTTP_201_CREATED)
def create_restroom(data: RestroomCreate, db: Session = Depends(get_db)):
    restroom = Restroom(
        building=data.building,
        floor=data.floor,
        type=data.type,
        latitude=data.latitude,
        longitude=data.longitude,
        crowd_level=data.crowd_level or "low",
    )
    db.add(restroom)
    db.commit()
    db.refresh(restroom)
    return restroom


@router.get("/restrooms/nearest")
def get_nearest_restroom(lat: float, lng: float, db: Session = Depends(get_db)):
    restrooms = db.query(Restroom).all()

    result = []

    for r in restrooms:
        distance = calculate_distance(lat, lng, r.latitude, r.longitude)

        result.append({
            "id": r.id,
            "building": r.building,
            "floor": r.floor,
            "type": r.type,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "distance_km": distance
        })

    result.sort(key=lambda x: x["distance_km"])

    return result[:5]  # เอา 5 ห้องน้ำที่ใกล้สุด


@router.get("/restrooms")
def get_all_restrooms(
    building: Optional[str] = None,
    floor: Optional[int] = None,
    restroom_type: Optional[str] = Query(None, alias="type"),
    db: Session = Depends(get_db),
):
    """ดึงรายการห้องน้ำทั้งหมด และสามารถกรองตาม building/floor/type ได้"""
    query = db.query(Restroom)

    if building:
        query = query.filter(Restroom.building == building)
    if floor is not None:
        query = query.filter(Restroom.floor == floor)
    if restroom_type:
        query = query.filter(Restroom.type == restroom_type)

    restrooms = query.all()
    return [
        {
            "id": r.id,
            "building": r.building,
            "floor": r.floor,
            "type": r.type,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "crowd_level": r.crowd_level,
        }
        for r in restrooms
    ]


@router.get("/restrooms/{restroom_id}")
def get_restroom_detail(restroom_id: int, db: Session = Depends(get_db)):
    """ดึงข้อมูลห้องน้ำตาม ID"""
    r = db.query(Restroom).filter(Restroom.id == restroom_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="ไม่พบห้องน้ำที่ระบุ")
    return {
        "id": r.id,
        "building": r.building,
        "floor": r.floor,
        "type": r.type,
        "latitude": r.latitude,
        "longitude": r.longitude,
        "crowd_level": r.crowd_level,
    }
