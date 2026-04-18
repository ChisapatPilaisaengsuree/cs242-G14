from datetime import datetime


def smart_search(keyword: str) -> dict:
    """
    แปลง keyword จาก user → dict ของ filter สำหรับ query DB
    เช่น "ห้องน้ำหญิง sc3 ชั้น 2" → {"type": "female", "building": "SC3", "floor": 2}
    """
    keyword = keyword.lower().strip()
    result = {}

    # --- ประเภทห้องน้ำ ---
    if "หญิง" in keyword or "female" in keyword or "women" in keyword or "ผู้หญิง" in keyword:
        result["type"] = "female"
    elif "ชาย" in keyword or "male" in keyword or "men" in keyword or "ผู้ชาย" in keyword:
        result["type"] = "male"
    elif "พิการ" in keyword or "disabled" in keyword or "wheelchair" in keyword:
        result["type"] = "disabled"

    # --- ชื่อตึก (เพิ่มได้ตามมหาวิทยาลัย) ---
    if "sc3" in keyword:
        result["building"] = "SC3"
    elif "eng" in keyword or "วิศวะ" in keyword:
        result["building"] = "ENG"
    elif "med" in keyword or "แพทย์" in keyword:
        result["building"] = "MED"

    # --- ชั้น ---
    for i in range(1, 20):
        if f"ชั้น {i}" in keyword or f"floor {i}" in keyword or f"ชั้น{i}" in keyword:
            result["floor"] = i
            break

    return result


def predict_crowd() -> str:
    """
    ทำนายความแออัดจากเวลาปัจจุบัน
    - high  : ชั่วโมงเร่งด่วน (พักเที่ยง / เลิกเรียน / ช่วงเช้า)
    - medium: ช่วงกลางวันปกติ
    - low   : เย็น / กลางคืน / เช้ามืด
    """
    hour = datetime.now().hour

    # ชั่วโมงเร่งด่วน: 7-9, 11-13, 16-18
    if (7 <= hour < 9) or (11 <= hour < 13) or (16 <= hour < 18):
        return "high"
    # ช่วงกลางวันปกติ: 9-11, 13-16
    elif (9 <= hour < 11) or (13 <= hour < 16):
        return "medium"
    # เย็น / กลางคืน / เช้ามืด
    else:
        return "low"
