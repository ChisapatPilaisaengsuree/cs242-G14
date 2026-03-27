# 🚀 Restroom Finder Backend (Python) - Project Guide

## 📌 Overview

โปรเจคนี้เป็นระบบ Backend สำหรับค้นหาห้องน้ำในมหาวิทยาลัย
โดยใช้ **Python (FastAPI)** และมีการใช้ **Machine Learning (เบื้องต้น)** เพื่อช่วยวิเคราะห์คำค้นและทำนายความแออัด

---

## 🎯 Objective

* ค้นหาห้องน้ำจาก keyword
* วิเคราะห์คำค้น (Smart Search)
* ทำนายความแออัด (Crowd Prediction)
* จัดอันดับห้องน้ำ (Ranking)
* แสดงผลลัพธ์ที่ดีที่สุดให้ผู้ใช้

---

## 🧠 System Flow

```
User Input → API → Smart Search (ML) → Query Database
→ Crowd Prediction → Ranking → Response
```

---

## 🧱 Project Structure

```
backend/
│
├── main.py
├── api/
│   └── search.py
│
├── database/
│   └── db.py
│
├── models/
│   └── restroom.py
│
├── schemas/
│   └── search_schema.py
│
├── services/
│   ├── search_service.py
│   ├── ranking.py
│   └── ml_model.py
```

---

## ⚙️ Step-by-Step Development

### 🔹 Step 1: Setup Project

* ติดตั้ง dependencies

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

* รัน server

```bash
uvicorn main:app --reload
```

---

### 🔹 Step 2: Database Design

สร้างตาราง `restrooms`

| Field       | Description      |
| ----------- | ---------------- |
| id          | รหัสห้องน้ำ      |
| building    | ตึก              |
| floor       | ชั้น             |
| type        | ชาย/หญิง/คนพิการ |
| latitude    | พิกัด            |
| longitude   | พิกัด            |
| crowd_level | ความแออัด        |

---

### 🔹 Step 3: API Endpoint

#### POST `/search`

**Request**

```json
{
  "keyword": "ห้องน้ำหญิง sc3"
}
```

**Response**

```json
[
  {
    "building": "SC3",
    "floor": 2,
    "type": "female",
    "crowd": "low"
  }
]
```

---

### 🔹 Step 4: Smart Search (ML)

แปลงคำค้น → filter

ตัวอย่าง:

```
"toilet female sc3"
→ type = female
→ building = sc3
```

---

### 🔹 Step 5: Query Database

ใช้ filter ค้นข้อมูลจาก DB

```sql
SELECT * FROM restrooms
WHERE type = 'female'
AND building = 'SC3'
```

---

### 🔹 Step 6: Crowd Prediction

ทำนายความแออัด:

* low
* medium
* high

ตัวอย่าง logic:

```
12:00 → high
09:00 → medium
```

---

### 🔹 Step 7: Ranking System

จัดอันดับโดย:

1. ความแออัด (low ก่อน)
2. (อนาคต) ระยะทาง

---

### 🔹 Step 8: Response

ส่งข้อมูลกลับ frontend ในรูปแบบ JSON

---

## 🧪 Testing

* ใช้ Swagger:

```
http://127.0.0.1:8000/docs
```

* ทดสอบ:

  * keyword ปกติ
  * keyword ผิด
  * ไม่มีข้อมูล

---

## 🌍 Future Improvements

* ใช้ ML จริง (NLP)
* เชื่อม Google Maps API
* เพิ่มระบบ Login (JWT)
* Deploy บน Cloud (AWS / Render)

---

## 💡 Notes

* เริ่มจากระบบง่ายก่อน (Search + DB)
* ค่อยเพิ่ม ML ทีหลัง
* อย่าทำทุกอย่างพร้อมกัน

---

## ✅ Status Checklist

* [ ] Setup Backend
* [ ] Create Database
* [ ] Build API
* [ ] Implement Search
* [ ] Add Ranking
* [ ] Add ML
* [ ] Deploy

---

## 🚀 Author

Project by: (ใส่ชื่อคุณ)

---
