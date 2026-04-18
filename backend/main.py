from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import routers
from api.search import router as search_router
from api.restroom import router as restroom_router

# สร้าง app
app = FastAPI(
    title="Restroom Finder API",
    description="API สำหรับค้นหาห้องน้ำในมหาวิทยาลัย",
    version="1.0.0"
)

# =========================
# 🔥 CORS (สำคัญมาก)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ตอน dev ใช้ * ไปก่อน
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 🔌 Include Routers
# =========================
app.include_router(search_router, prefix="/api")
app.include_router(restroom_router, prefix="/api")

# =========================
# 🌱 Startup — สร้าง DB + seed ข้อมูล
# =========================
@app.on_event("startup")
def startup_event():
    from database.init_db import init_db
    init_db()

# =========================
# 🏠 Root Endpoint
# =========================
@app.get("/")
def root():
    return {
        "message": "Restroom Finder Backend is running 🚀",
        "docs": "/docs",
    }

# =========================
# ⚡ Health Check
# =========================
@app.get("/health")
def health_check():
    return {"status": "ok"}
