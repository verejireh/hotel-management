from fastapi import APIRouter, Depends
from datetime import date
from app.models import CheckInOutSummary, Reservation
from app.db import MySQLDB
from app.utils import get_today_checkins, get_today_checkouts, reservation_dict_to_model

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


def get_db():
    return MySQLDB()


@router.get("/checkin-out", response_model=CheckInOutSummary)
async def get_checkin_checkout_summary(db: MySQLDB = Depends(get_db)):
    """오늘의 체크인/체크아웃 명부"""
    reservations_data = db.get_reservations()
    
    checkins_data = get_today_checkins(reservations_data)
    checkouts_data = get_today_checkouts(reservations_data)
    
    checkins = [reservation_dict_to_model(r) for r in checkins_data]
    checkouts = [reservation_dict_to_model(r) for r in checkouts_data]
    
    return CheckInOutSummary(
        check_ins=checkins,
        check_outs=checkouts,
        date=date.today()
    )


@router.get("/stats")
async def get_dashboard_stats(db: MySQLDB = Depends(get_db)):
    """대시보드 통계"""
    reservations_data = db.get_reservations()
    rooms_data = db.get_rooms()
    
    today = date.today()
    today_str = str(today)
    
    # 오늘 체크인/체크아웃 수
    checkins = get_today_checkins(reservations_data)
    checkouts = get_today_checkouts(reservations_data)
    
    # 전체 예약 수
    total_reservations = len(reservations_data)
    active_reservations = len([r for r in reservations_data if r.get('status') in ['confirmed', 'checked_in']])
    
    # 방 상태별 통계
    total_rooms = len(rooms_data)
    available_rooms = len([r for r in rooms_data if r.get('status') == 'available'])
    occupied_rooms = len([r for r in rooms_data if r.get('status') == 'occupied'])
    
    return {
        "today_checkins": len(checkins),
        "today_checkouts": len(checkouts),
        "total_reservations": total_reservations,
        "active_reservations": active_reservations,
        "total_rooms": total_rooms,
        "available_rooms": available_rooms,
        "occupied_rooms": occupied_rooms,
        "occupancy_rate": round((occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0, 2)
    }






