from backend.database.db import engine, SessionLocal, Base
from backend.models.restroom import Restroom


def init_db():
    """
    สร้างตาราง database และใส่ข้อมูล sample ถ้ายังว่างอยู่
    เรียกใช้ตอน startup ใน main.py
    """
    # สร้างตารางทั้งหมดจาก Model
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # ตรวจว่ามีข้อมูลแล้วหรือยัง ถ้ามีแล้วไม่ต้อง insert ซ้ำ
        if db.query(Restroom).count() > 0:
            print("✅ Database already has data. Skipping seed.")
            return

        print("🌱 Seeding database with sample restroom data...")

        # ============================================================
        # ⚠️  TODO: ใส่ข้อมูลห้องน้ำจริงของมหาวิทยาลัยตรงนี้
        #     ดูคำอธิบายแต่ละ field ด้านล่าง
        # ============================================================
        sample_data = [
            # --- ตึก SC3 ---
            Restroom(building="SC3", floor=1, type="male",     latitude=14.0704, longitude=100.6057, crowd_level="low"),
            Restroom(building="SC3", floor=1, type="female",   latitude=14.0704, longitude=100.6057, crowd_level="low"),
            Restroom(building="SC3", floor=2, type="female",   latitude=14.0704, longitude=100.6057, crowd_level="medium"),
            Restroom(building="SC3", floor=2, type="male",     latitude=14.0704, longitude=100.6057, crowd_level="medium"),
            Restroom(building="SC3", floor=1, type="disabled", latitude=14.0704, longitude=100.6057, crowd_level="low"),
 
            # --- ยิม 7 ---
            Restroom(building="ยิม7", floor=1, type="female",  latitude=14.0712, longitude=100.6070, crowd_level="high"),
            Restroom(building="ยิม7", floor=1, type="male",    latitude=14.0712, longitude=100.6070, crowd_level="high"),
 
            # --- บร5 ---
            Restroom(building="บร5", floor=1, type="male",     latitude=14.0695, longitude=100.6048, crowd_level="high"),
            Restroom(building="บร5", floor=2, type="female",   latitude=14.0695, longitude=100.6048, crowd_level="low"),
 
            # --- SC2 ---
            Restroom(building="SC2", floor=1, type="male",     latitude=14.0698, longitude=100.6052, crowd_level="high"),
            Restroom(building="SC2", floor=3, type="female",   latitude=14.0698, longitude=100.6052, crowd_level="low"),

            # --- SC1 ---
            Restroom(building="SC1", floor=1, type="mixed",    latitude=14.0690, longitude=100.6049, crowd_level="high"),
            Restroom(building="SC1", floor=2, type="female",   latitude=14.0690, longitude=100.6049, crowd_level="medium"),
            Restroom(building="SC1", floor=3, type="male",     latitude=14.0690, longitude=100.6049, crowd_level="low"),
        ]

        db.add_all(sample_data)
        db.commit()
        print(f"✅ Seeded {len(sample_data)} restrooms successfully.")

    finally:
        db.close()
