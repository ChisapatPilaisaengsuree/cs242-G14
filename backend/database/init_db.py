from database.db import engine, SessionLocal, Base
from models.restroom import Restroom


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
            Restroom(building="SC3", floor=1, type="male",     latitude=13.7467, longitude=100.5331, crowd_level="low"),
            Restroom(building="SC3", floor=2, type="female",   latitude=13.7467, longitude=100.5331, crowd_level="medium"),
            Restroom(building="SC3", floor=2, type="male",     latitude=13.7467, longitude=100.5331, crowd_level="medium"),
            Restroom(building="SC3", floor=2, type="disabled", latitude=13.7467, longitude=100.5331, crowd_level="low"),

            # --- ตึก ENG ---
            Restroom(building="ENG", floor=1, type="female",   latitude=13.7480, longitude=100.5340, crowd_level="high"),
            Restroom(building="ENG", floor=1, type="male",     latitude=13.7480, longitude=100.5340, crowd_level="high"),
            Restroom(building="ENG", floor=3, type="female",   latitude=13.7480, longitude=100.5340, crowd_level="medium"),
            Restroom(building="ENG", floor=3, type="male",     latitude=13.7480, longitude=100.5340, crowd_level="low"),

            # --- ตึก MED ---
            Restroom(building="MED", floor=1, type="female",   latitude=13.7460, longitude=100.5320, crowd_level="low"),
            Restroom(building="MED", floor=1, type="male",     latitude=13.7460, longitude=100.5320, crowd_level="medium"),
            Restroom(building="MED", floor=1, type="disabled", latitude=13.7460, longitude=100.5320, crowd_level="low"),
        ]

        db.add_all(sample_data)
        db.commit()
        print(f"✅ Seeded {len(sample_data)} restrooms successfully.")

    finally:
        db.close()
