PLACES = [
    {
        "id": "sc3",
        "name": "อาคาร SC3",
        "lat": 14.0703,
        "lng": 100.6058,
        "toilets": [
            {"id": 1,  "name": "SC3 ชั้น 1 - หญิง",    "floor": "ชั้น 1", "gender": "Female",   "distance": 85,  "occupancy": 22, "capacity": 8},
            {"id": 2,  "name": "SC3 ชั้น 1 - ชาย",     "floor": "ชั้น 1", "gender": "Male",     "distance": 90,  "occupancy": 15, "capacity": 8},
            {"id": 3,  "name": "SC3 ชั้น 2 - หญิง",    "floor": "ชั้น 2", "gender": "Female",   "distance": 120, "occupancy": 68, "capacity": 8},
            {"id": 4,  "name": "SC3 ชั้น 2 - ชาย",     "floor": "ชั้น 2", "gender": "Male",     "distance": 125, "occupancy": 30, "capacity": 6},
            {"id": 11, "name": "SC3 ชั้น 1 - คนพิการ", "floor": "ชั้น 1", "gender": "Disabled", "distance": 88,  "occupancy": 0,  "capacity": 2},
        ],
    },
    {
        "id": "gym7",
        "name": "อาคารยิม7",
        "lat": 14.0712,
        "lng": 100.6070,
        "toilets": [
            {"id": 5, "name": "ยิม7 ชั้น 1 - หญิง", "floor": "ชั้น 1", "gender": "Female", "distance": 210, "occupancy": 75, "capacity": 6},
            {"id": 6, "name": "ยิม7 ชั้น 1 - ชาย",  "floor": "ชั้น 1", "gender": "Male",   "distance": 215, "occupancy": 40, "capacity": 6},
        ],
    },
    {
        "id": "br5",
        "name": "อาคาร บร5",
        "lat": 14.0695,
        "lng": 100.6048,
        "toilets": [
            {"id": 7, "name": "บร5 ชั้น 1 - ชาย",  "floor": "ชั้น 1", "gender": "Male",   "distance": 85,  "occupancy": 92, "capacity": 10},
            {"id": 8, "name": "บร5 ชั้น 2 - หญิง", "floor": "ชั้น 2", "gender": "Female", "distance": 90,  "occupancy": 10, "capacity": 6},
        ],
    },
    {
        "id": "sc2",
        "name": "อาคาร SC2",
        "lat": 14.0698,
        "lng": 100.6052,
        "toilets": [
            {"id": 9,  "name": "SC2 ชั้น 1 - ชาย",  "floor": "ชั้น 1", "gender": "Male",   "distance": 320, "occupancy": 90, "capacity": 10},
            {"id": 10, "name": "SC2 ชั้น 3 - หญิง", "floor": "ชั้น 3", "gender": "Female", "distance": 340, "occupancy": 10, "capacity": 6},
        ],
    },
]

USERS = [
    {"email": "user@tu.ac.th",  "password": "1234",  "role": "user",  "name": "นักศึกษา TU"},
    {"email": "admin@tu.ac.th", "password": "admin", "role": "admin", "name": "ผู้ดูแลระบบ"},
]

# helper functions
def get_status(occupancy):
    if occupancy <= 40:
        return "available"
    elif occupancy <= 75:
        return "busy"
    return "crowded"

def get_status_label(occupancy):
    s = get_status(occupancy)
    return {"available": "ว่าง", "busy": "ค่อนข้างเต็ม", "crowded": "เต็ม"}[s]

def get_status_color(occupancy):
    s = get_status(occupancy)
    return {"available": "#16a34a", "busy": "#d97706", "crowded": "#dc2626"}[s]

def get_gender_icon(gender):
    return {"Female": "♀", "Male": "♂", "Disabled": "♿"}.get(gender, "🚻")

def get_gender_label(gender):
    return {"Female": "หญิง", "Male": "ชาย", "Disabled": "คนพิการ"}.get(gender, "")

def get_gender_color(gender):
    return {"Female": "#db2777", "Male": "#2563eb", "Disabled": "#7c3aed"}.get(gender, "#888")

def flat_toilets(places):
    result = []
    for p in places:
        for t in p["toilets"]:
            result.append({**t, "place_id": p["id"], "place_name": p["name"], "lat": p["lat"], "lng": p["lng"]})
    return result