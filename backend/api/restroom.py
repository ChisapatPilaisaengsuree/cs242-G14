from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.search_service import calculate_distance
from database.db import get_db
from models.restroom import Restroom

router = APIRouter()

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
def get_all_restrooms(db: Session = Depends(get_db)):
    """ดึงรายการห้องน้ำทั้งหมด"""
    restrooms = db.query(Restroom).all()
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
