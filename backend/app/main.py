from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import reservations, rooms, dashboard, calendar, revenue, customers, checkinout, cleaning, reports, admins, room_notes
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Hotel Management API",
    description="호텔 관리자 페이지 API - 여러 예약 플랫폼 통합 관리",
    version="1.0.0"
)

# CORS 설정
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(reservations.router)
app.include_router(rooms.router)
app.include_router(dashboard.router)
app.include_router(calendar.router)
app.include_router(revenue.router)
app.include_router(customers.router)
app.include_router(checkinout.router)
app.include_router(cleaning.router)
app.include_router(reports.router)
app.include_router(admins.router)
app.include_router(room_notes.router)


@app.get("/")
async def root():
    return {
        "message": "Hotel Management API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

