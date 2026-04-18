from database.db import SessionLocal
from models.restroom import Restroom
from services.ml_model import smart_search, predict_crowd
from services.ranking import rank_results


def search_restrooms(keyword: str):
    db = SessionLocal()
    try:
        # แปลง keyword → filters ด้วย ML/Rule-based
        filters = smart_search(keyword)

        query = db.query(Restroom)

        if "type" in filters:
            query = query.filter(Restroom.type == filters["type"])

        if "building" in filters:
            query = query.filter(Restroom.building == filters["building"])

        if "floor" in filters:
            query = query.filter(Restroom.floor == filters["floor"])

        restrooms = query.all()

        # predict crowd level สำหรับห้องน้ำแต่ละห้อง
        for r in restrooms:
            r.crowd_level = predict_crowd()

        # จัดอันดับ (low crowd ก่อน)
        ranked = rank_results(restrooms)

        result = [
            {
                "id": r.id,
                "building": r.building,
                "floor": r.floor,
                "type": r.type,
                "latitude": r.latitude,
                "longitude": r.longitude,
                "crowd": r.crowd_level,
            }
            for r in ranked
        ]
        return result

    finally:
        db.close()  # ปิด session เสมอ ไม่ว่าจะ error หรือไม่
