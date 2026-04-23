from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import router ก่อน
from api.search import router as search_router
from api.restroom import router as restroom_router

# สร้าง app ก่อน
app = FastAPI(
    title="Restroom Finder API",
    description="API สำหรับค้นหาห้องน้ำ",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include router หลังจากมี app แล้ว
app.include_router(search_router, prefix="/api")
app.include_router(restroom_router, prefix="/api")


# startup
@app.on_event("startup")
def startup_event():
    from database.init_db import init_db
    init_db()


# root
@app.get("/")
def root():
    return {
        "message": "Restroom Finder Backend is running 🚀",
        "docs": "/docs"
    }


# health
@app.get("/health")
def health_check():
    return {"status": "ok"}