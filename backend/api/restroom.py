from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.restroom import Restroom

router = APIRouter()


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
