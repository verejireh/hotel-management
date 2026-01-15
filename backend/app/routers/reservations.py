from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from datetime import date
from app.models import Reservation, ReservationCreate
from app.db import MySQLDB
from app.utils import reservation_dict_to_model, parse_date

router = APIRouter(prefix="/api/reservations", tags=["reservations"])


def get_db():
    return MySQLDB()


@router.get("/", response_model=List[Reservation])
async def get_reservations(db: MySQLDB = Depends(get_db)):
    """모든 예약 조회"""
    reservations_data = db.get_reservations()
    return [reservation_dict_to_model(r) for r in reservations_data]


@router.get("/{reservation_id}", response_model=Reservation)
async def get_reservation(reservation_id: str, db: MySQLDB = Depends(get_db)):
    """예약 상세 조회"""
    reservation_data = db.get_reservation(reservation_id)
    if not reservation_data:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation_dict_to_model(reservation_data)


@router.post("/", response_model=Reservation)
async def create_reservation(reservation: ReservationCreate, db: MySQLDB = Depends(get_db)):
    """새 예약 생성 (중복 체크 포함)"""
    # 중복 예약 체크
    check_in_str = str(reservation.check_in)
    check_out_str = str(reservation.check_out)
    
    if db.check_duplicate_reservation(reservation.room_id, check_in_str, check_out_str):
        raise HTTPException(
            status_code=400,
            detail="Room is already booked for the selected dates"
        )
    
    # 예약 생성
    reservation_dict = reservation.dict()
    reservation_dict['created_at'] = str(date.today())
    # 기본 status를 'Reserved'로 설정
    if 'status' not in reservation_dict or not reservation_dict.get('status'):
        reservation_dict['status'] = 'Reserved'
    new_reservation = db.create_reservation(reservation_dict)
    
    # 방 상태 업데이트
    db.update_room_status(reservation.room_id, "occupied")
    
    return reservation_dict_to_model(new_reservation)


@router.get("/room/{room_id}/availability")
async def check_room_availability(room_id: str, check_in: date, check_out: date, db: MySQLDB = Depends(get_db)):
    """방 가용성 체크"""
    check_in_str = str(check_in)
    check_out_str = str(check_out)
    
    is_available = not db.check_duplicate_reservation(room_id, check_in_str, check_out_str)
    
    return {
        "room_id": room_id,
        "check_in": check_in_str,
        "check_out": check_out_str,
        "available": is_available
    }


@router.put("/{reservation_id}/status")
async def update_reservation_status(
    reservation_id: str, 
    status: str = Query(..., description="Status: Reserved, Checked in, or Checked out"),
    db: MySQLDB = Depends(get_db)
):
    """예약 Status 업데이트"""
    # URL 디코딩된 status 값 정리
    status = status.strip()
    
    valid_statuses = ['Reserved', 'Checked in', 'Checked out']
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status: '{status}'. Must be one of: {', '.join(valid_statuses)}"
        )
    
    reservation_data = db.get_reservation(reservation_id)
    if not reservation_data:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    try:
        # 예약 Status 업데이트
        db.update_reservation_status(reservation_id, status)
        
        # rooms 시트의 Status도 업데이트
        room_id = reservation_data.get('room_id', '')
        if room_id:
            # Status에 따라 rooms 시트의 status 매핑
            room_status_map = {
                'Reserved': 'occupied',
                'Checked in': 'occupied',
                'Checked out': 'available'
            }
            room_status = room_status_map.get(status, 'occupied')
            db.update_room_status(room_id, room_status)
        
        updated_reservation = db.get_reservation(reservation_id)
        return reservation_dict_to_model(updated_reservation)
    except Exception as e:
        print(f"Error updating reservation status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update status: {str(e)}")

