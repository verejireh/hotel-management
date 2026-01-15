from fastapi import APIRouter, Depends
from typing import List, Dict
from datetime import date, datetime, timedelta
from app.db import MySQLDB
from app.utils import parse_date

router = APIRouter(prefix="/api/revenue", tags=["revenue"])


def get_db():
    return MySQLDB()


@router.get("/daily/{start_date}/{end_date}")
async def get_daily_revenue(start_date: str, end_date: str, db: MySQLDB = Depends(get_db)):
    """일별 수익 통계"""
    start = parse_date(start_date)
    end = parse_date(end_date)
    
    reservations_data = db.get_reservations()
    
    daily_revenue = {}
    current_date = start
    
    while current_date <= end:
        daily_revenue[str(current_date)] = {
            "date": str(current_date),
            "revenue": 0.0,
            "reservations": 0,
            "check_ins": 0,
            "check_outs": 0
        }
        current_date += timedelta(days=1)
    
    for res_data in reservations_data:
        try:
            check_in = parse_date(res_data.get('check_in', ''))
            check_out = parse_date(res_data.get('check_out', ''))
            total_price = float(res_data.get('total_price', 0))
            status = res_data.get('status', '')
            
            # 체크인 날짜별 수익 계산
            if start <= check_in <= end:
                date_str = str(check_in)
                if date_str in daily_revenue:
                    daily_revenue[date_str]["revenue"] += total_price
                    daily_revenue[date_str]["check_ins"] += 1
                    if status in ['confirmed', 'checked_in']:
                        daily_revenue[date_str]["reservations"] += 1
            
            # 체크아웃 날짜별 통계
            if start <= check_out <= end:
                date_str = str(check_out)
                if date_str in daily_revenue:
                    daily_revenue[date_str]["check_outs"] += 1
        except:
            continue
    
    return {
        "start_date": start_date,
        "end_date": end_date,
        "daily_data": list(daily_revenue.values())
    }


@router.get("/monthly/{year}")
async def get_monthly_revenue(year: int, db: MySQLDB = Depends(get_db)):
    """월별 수익 통계"""
    monthly_revenue = {}
    
    for month in range(1, 13):
        monthly_revenue[month] = {
            "year": year,
            "month": month,
            "revenue": 0.0,
            "reservations": 0,
            "check_ins": 0,
            "check_outs": 0
        }
    
    reservations_data = db.get_reservations()
    
    for res_data in reservations_data:
        try:
            check_in = parse_date(res_data.get('check_in', ''))
            total_price = float(res_data.get('total_price', 0))
            status = res_data.get('status', '')
            
            if check_in.year == year:
                month = check_in.month
                monthly_revenue[month]["revenue"] += total_price
                monthly_revenue[month]["check_ins"] += 1
                if status in ['confirmed', 'checked_in']:
                    monthly_revenue[month]["reservations"] += 1
        except:
            continue
    
    return {
        "year": year,
        "monthly_data": list(monthly_revenue.values())
    }


@router.get("/platform/{start_date}/{end_date}")
async def get_platform_revenue(start_date: str, end_date: str, db: MySQLDB = Depends(get_db)):
    """플랫폼별 수익 통계"""
    start = parse_date(start_date)
    end = parse_date(end_date)
    
    reservations_data = db.get_reservations()
    platforms_data = db.get_platforms()
    
    platform_map = {p.get('id', ''): p.get('name', 'Unknown') for p in platforms_data}
    
    platform_revenue = {}
    
    for res_data in reservations_data:
        try:
            check_in = parse_date(res_data.get('check_in', ''))
            platform_id = res_data.get('platform_id', '')
            total_price = float(res_data.get('total_price', 0))
            
            if start <= check_in <= end:
                platform_name = platform_map.get(platform_id, f"Platform {platform_id}")
                
                if platform_name not in platform_revenue:
                    platform_revenue[platform_name] = {
                        "platform": platform_name,
                        "platform_id": platform_id,
                        "revenue": 0.0,
                        "reservations": 0
                    }
                
                platform_revenue[platform_name]["revenue"] += total_price
                platform_revenue[platform_name]["reservations"] += 1
        except:
            continue
    
    return {
        "start_date": start_date,
        "end_date": end_date,
        "platform_data": list(platform_revenue.values())
    }






