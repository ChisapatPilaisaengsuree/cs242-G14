from database.db import SessionLocal
from models.restroom import Restroom
from services.ml_model import smart_search, predict_crowd
from services.ranking import rank_results

def search_restrooms(keyword: str):
    db = SessionLocal()

    filters = smart_search(keyword)

    query = db.query(Restroom)

    if "type" in filters:
        query = query.filter(Restroom.type == filters["type"])

    if "building" in filters:
        query = query.filter(Restroom.building == filters["building"])

    restrooms = query.all()

    # predict crowd
    for r in restrooms:
        r.crowd_level = predict_crowd()

    ranked = rank_results(restrooms)

    result = []
    for r in ranked:
        result.append({
            "building": r.building,
            "floor": r.floor,
            "type": r.type,
            "crowd": r.crowd_level
        })

    return result