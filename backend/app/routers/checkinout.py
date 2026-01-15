from fastapi import APIRouter, HTTPException, Depends
from app.db import MySQLDB
from app.utils import reservation_dict_to_model
from typing import List

router = APIRouter(prefix="/api/checkinout", tags=["checkinout"])


def get_db():
    return MySQLDB()


@router.post("/checkin/{reservation_id}")
async def check_in(reservation_id: str, db: MySQLDB = Depends(get_db)):
    """체크인 처리"""
    reservation_data = db.get_reservation(reservation_id)
    if not reservation_data:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    # 상태 업데이트
    current_status = reservation_data.get('status', '')
    if current_status == 'Checked in':
        raise HTTPException(status_code=400, detail="Already checked in")
    
    # 예약 상태 업데이트
    db.update_reservation_status(reservation_id, "Checked in")
    
    # 방 상태도 업데이트
    room_id = reservation_data.get('room_id', '')
    if room_id:
        db.update_room_status(room_id, "occupied")
    
    # 업데이트된 예약 반환
    updated_reservation = db.get_reservation(reservation_id)
    return reservation_dict_to_model(updated_reservation)


@router.post("/checkout/{reservation_id}")
async def check_out(reservation_id: str, db: MySQLDB = Depends(get_db)):
    """체크아웃 처리"""
    reservation_data = db.get_reservation(reservation_id)
    if not reservation_data:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    current_status = reservation_data.get('status', '')
    if current_status == 'Checked out':
        raise HTTPException(status_code=400, detail="Already checked out")
    
    # 예약 상태 업데이트
    db.update_reservation_status(reservation_id, "Checked out")
    
    # 방 상태 업데이트 (청소 필요)
    room_id = reservation_data.get('room_id', '')
    if room_id:
        db.update_room_status(room_id, "cleaning")
    
    # 업데이트된 예약 반환
    updated_reservation = db.get_reservation(reservation_id)
    return reservation_dict_to_model(updated_reservation)


@router.get("/upcoming")
async def get_upcoming_checkins_checkouts(days: int = 7, db: MySQLDB = Depends(get_db)):
    """다가오는 체크인/체크아웃 목록"""
    from datetime import date, timedelta
    from app.utils import parse_date
    
    today = date.today()
    end_date = today + timedelta(days=days)
    
    reservations_data = db.get_reservations()
    
    upcoming_checkins = []
    upcoming_checkouts = []
    
    for res_data in reservations_data:
        try:
            check_in = parse_date(res_data.get('check_in', ''))
            check_out = parse_date(res_data.get('check_out', ''))
            status = res_data.get('status', '')
            
            if status in ['confirmed'] and today <= check_in <= end_date:
                reservation = reservation_dict_to_model(res_data)
                upcoming_checkins.append(reservation)
            
            if status in ['confirmed', 'checked_in'] and today <= check_out <= end_date:
                reservation = reservation_dict_to_model(res_data)
                upcoming_checkouts.append(reservation)
        except:
            continue
    
    return {
        "days": days,
        "upcoming_checkins": upcoming_checkins,
        "upcoming_checkouts": upcoming_checkouts
    }

