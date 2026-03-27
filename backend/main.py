from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import router
from api.search import router as search_router

# สร้าง app
app = FastAPI(
    title="Restroom Finder API",
    description="API สำหรับค้นหาห้องน้ำ",
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
# 🔌 Include Router
# =========================
app.include_router(search_router, prefix="/api")

# =========================
# 🏠 Root Endpoint
# =========================
@app.get("/")
def root():
    return {
        "message": "Restroom Finder Backend is running 🚀"
    }

# =========================
# ⚡ Health Check
# =========================
@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }