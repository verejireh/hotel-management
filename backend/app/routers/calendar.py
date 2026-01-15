from fastapi import APIRouter, Depends
from typing import List
from datetime import date, datetime
from app.db import MySQLDB
from app.utils import reservation_dict_to_model

router = APIRouter(prefix="/api/calendar", tags=["calendar"])


def get_db():
    return MySQLDB()


@router.get("/month/{year}/{month}")
async def get_month_reservations(year: int, month: int, db: MySQLDB = Depends(get_db)):
    """월별 예약 현황 조회"""
    reservations_data = db.get_reservations()
    
    # 해당 월의 예약만 필터링
    month_reservations = []
    for res_data in reservations_data:
        try:
            check_in_str = res_data.get('check_in', '')
            check_out_str = res_data.get('check_out', '')
            
            if not check_in_str or not check_out_str:
                continue
            
            # 날짜 파싱
            from app.utils import parse_date
            check_in = parse_date(check_in_str)
            check_out = parse_date(check_out_str)
            
            # 해당 월과 겹치는 예약 찾기
            start_month = date(year, month, 1)
            if month == 12:
                end_month = date(year + 1, 1, 1)
            else:
                end_month = date(year, month + 1, 1)
            
            if check_in < end_month and check_out >= start_month:
                reservation = reservation_dict_to_model(res_data)
                month_reservations.append(reservation)
        except:
            continue
    
    return {
        "year": year,
        "month": month,
        "reservations": month_reservations
    }


@router.get("/week/{year}/{week}")
async def get_week_reservations(year: int, week: int, db: MySQLDB = Depends(get_db)):
    """주별 예약 현황 조회"""
    from datetime import timedelta
    
    # 주의 첫날 계산
    jan1 = date(year, 1, 1)
    days_offset = (week - 1) * 7
    week_start = jan1 + timedelta(days=jan1.weekday() - days_offset)
    week_end = week_start + timedelta(days=6)
    
    reservations_data = db.get_reservations()
    
    week_reservations = []
    for res_data in reservations_data:
        try:
            from app.utils import parse_date
            check_in = parse_date(res_data.get('check_in', ''))
            check_out = parse_date(res_data.get('check_out', ''))
            
            if check_in <= week_end and check_out >= week_start:
                reservation = reservation_dict_to_model(res_data)
                week_reservations.append(reservation)
        except:
            continue
    
    return {
        "year": year,
        "week": week,
        "week_start": str(week_start),
        "week_end": str(week_end),
        "reservations": week_reservations
    }






