# 🚀 Restroom Finder Backend (Python)

### Smart Search & Crowd Prediction System

---

## 📌 Overview

ระบบนี้เป็น **Backend API** สำหรับค้นหาห้องน้ำในมหาวิทยาลัย
โดยใช้ **Python (FastAPI)** และมีการใช้แนวคิด **Machine Learning (ML)** เพื่อเพิ่มความฉลาดของระบบ

ระบบสามารถ:

* ค้นหาห้องน้ำจาก keyword
* วิเคราะห์คำค้น (แม้พิมพ์ไม่ตรง)
* ทำนายความแออัด
* จัดอันดับห้องน้ำที่เหมาะสมที่สุด

---

## 🎯 Objective

* ลดเวลาการหาห้องน้ำ
* แนะนำห้องน้ำที่ “ดีที่สุด” ให้ผู้ใช้
* รองรับการค้นหาหลายรูปแบบ (ไทย / อังกฤษ)
* พัฒนาเป็นระบบอัจฉริยะในอนาคต (ML เต็มรูปแบบ)

---

## 🧠 System Flow

```
User Input
   ↓
API (FastAPI)
   ↓
Smart Search (ML)
   ↓
Query Database
   ↓
Crowd Prediction
   ↓
Ranking System
   ↓
Response (JSON)
```

---

## 🧱 Project Structure

```
backend/
│
├── main.py                # Entry point
│
├── api/                   # Route layer (รับ request)
│   └── search.py
│
├── database/              # Database connection
│   └── db.py
│
├── models/                # Table structure
│   └── restroom.py
│
├── schemas/               # Data validation
│   └── search_schema.py
│
├── services/              # Business logic
│   ├── search_service.py  # Logic หลัก
│   ├── ranking.py         # จัดอันดับ
│   └── ml_model.py        # Smart Search + Prediction
│
└── requirements.txt
```

---

# ⚙️ Development Guide (สิ่งที่ต้องทำทีละส่วน)

---

## 🔥 1. main.py (Core System)

### 🎯 หน้าที่

* เป็นตัวเริ่มต้นของระบบ
* รวมทุก API

### ✅ ทีมต้องทำ:

* [ ] เพิ่ม router ใหม่ (future: auth, user)
* [ ] ตั้งค่า CORS (รองรับ frontend)
* [ ] เพิ่ม startup/shutdown event

---

## 🔌 2. api/search.py (API Layer)

### 🎯 หน้าที่

* รับ request จาก user
* ส่งต่อไป service

### ✅ ทีมต้องทำ:

* [ ] ตรวจสอบ input (validation)
* [ ] handle error
* [ ] รองรับ parameter เพิ่ม เช่น:

  * location
  * type
  * building

---

## 🗄️ 3. database/db.py (Database)

### 🎯 หน้าที่

* เชื่อมต่อ database

### ✅ ทีมต้องทำ:

* [ ] ตั้งค่า SQLite (phase แรก)
* [ ] เปลี่ยนเป็น PostgreSQL (deploy)
* [ ] จัดการ session ให้ปลอดภัย

---

## 🚽 4. models/restroom.py (Data Model)

### 🎯 หน้าที่

* โครงสร้างข้อมูลห้องน้ำ

### ✅ ทีมต้องทำ:

* [ ] เพิ่ม field:

  * opening_hours
  * rating
  * description
* [ ] เพิ่ม index (เพิ่มความเร็ว query)

---

## 📥 5. schemas/ (Validation Layer)

### 🎯 หน้าที่

* กำหนดรูปแบบ input/output

### ✅ ทีมต้องทำ:

* [ ] แยก Request / Response
* [ ] validate type (string, int)
* [ ] ป้องกัน input ผิด format

---

## 🧠 6. services/ml_model.py (AI Layer)

### 🎯 หน้าที่

* วิเคราะห์คำค้น
* ทำนายความแออัด

### ✅ ทีมต้องทำ:

### 🔹 Smart Search

* [ ] รองรับ:

  * ไทย / อังกฤษ
  * คำพิมพ์ผิด
* [ ] mapping keyword → filter

### 🔹 Crowd Prediction

* [ ] ใช้ rule-based (phase 1)
* [ ] ใช้ data จริง (phase 2)
* [ ] train ML model (phase 3)

---

## 📊 7. services/ranking.py (Ranking System)

### 🎯 หน้าที่

* จัดอันดับผลลัพธ์

### ✅ ทีมต้องทำ:

* [ ] เรียงจาก crowd:

  * low → medium → high
* [ ] เพิ่ม distance (future)
* [ ] ทำ score system

### 🔥 Example:

```
score = (crowd_weight * 0.7) + (distance * 0.3)
```

---

## 🔍 8. services/search_service.py (Main Logic)

### 🎯 หน้าที่ (สำคัญที่สุด)

* รวมทุกระบบเข้าด้วยกัน

### Flow:

```
keyword → ML → filter → DB → predict → rank → response
```

### ✅ ทีมต้องทำ:

* [ ] เชื่อม ML + DB
* [ ] optimize query
* [ ] แยก logic ให้ clean
* [ ] handle edge cases

---

## 🧪 9. Testing

### 🎯 หน้าที่

* ทำให้ระบบเสถียร

### ✅ ทีมต้องทำ:

* [ ] test keyword ปกติ
* [ ] test keyword ผิด
* [ ] test ไม่มีข้อมูล
* [ ] test performance

---

## 🌍 10. External API

### 🎯 หน้าที่

* ใช้ข้อมูลภายนอก

### ✅ ทีมต้องทำ:

* [ ] เชื่อม Google Maps API
* [ ] คำนวณ distance
* [ ] เพิ่ม location-based search

---

## 🔐 11. Security (Advanced)

### 🎯 หน้าที่

* ป้องกันระบบ

### ✅ ทีมต้องทำ:

* [ ] JWT Authentication
* [ ] Rate limiting
* [ ] Input sanitization

---

## 🚀 12. Deployment

### 🎯 หน้าที่

* ใช้งานจริง

### ✅ ทีมต้องทำ:

* [ ] ตั้งค่า environment (.env)
* [ ] ใช้ PostgreSQL
* [ ] deploy (Render / AWS)

---

# 📊 Database Design

| Field       | Description |
| ----------- | ----------- |
| id          | รหัส        |
| building    | ตึก         |
| floor       | ชั้น        |
| type        | ชาย/หญิง    |
| latitude    | พิกัด       |
| longitude   | พิกัด       |
| crowd_level | ความแออัด   |

---

# 🔌 API Example

## POST `/search`

### Request

```json
{
  "keyword": "ห้องน้ำหญิง sc3"
}
```

### Response

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

# 🧭 Roadmap

## 🟢 Phase 1 (MVP)

* [ ] สร้าง API
* [ ] เชื่อม DB
* [ ] ค้นหาได้

## 🟡 Phase 2 (Smart System)

* [ ] Smart Search
* [ ] Ranking
* [ ] Crowd Prediction

## 🔴 Phase 3 (Production)

* [ ] ML จริง
* [ ] Map API
* [ ] Deploy

---

# 💡 Key Insight

> ❌ อย่าเริ่มจาก ML
> ✅ เริ่มจาก “ระบบค้นหาให้ทำงานได้ก่อน”

---

# 👥 Team Responsibility (สำคัญมาก)

| Role         | Responsibility            |
| ------------ | ------------------------- |
| Backend Dev  | API + DB + Logic          |
| ML Dev       | Smart Search + Prediction |
| Frontend Dev | UI + Map                  |
| DevOps       | Deploy + Server           |

---

# 🚀 Author

Project by: (ใส่ชื่อทีม/คุณ)

---
