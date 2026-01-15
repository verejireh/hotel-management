from datetime import date, datetime
from typing import List, Dict
from app.models import Reservation


def parse_date(date_str: str) -> date:
    """문자열을 date 객체로 변환"""
    if isinstance(date_str, date):
        return date_str
    if isinstance(date_str, datetime):
        return date_str.date()
    
    if not date_str:
        raise ValueError("Empty date string")
    
    date_str = str(date_str).strip()
    
    # 여러 날짜 형식 지원
    formats = [
        '%Y-%m-%d',      # 2026-01-02
        '%Y/%m/%d',      # 2026/01/02
        '%d/%m/%Y',      # 02/01/2026
        '%m/%d/%Y',      # 01/02/2026
        '%Y%m%d',        # 20260102 (YYYYMMDD)
        '%d-%m-%Y',      # 02-01-2026
        '%m-%d-%Y',      # 01-02-2026
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except:
            continue
    
    raise ValueError(f"Unable to parse date: {date_str}")


def get_today_checkins(reservations: List[Dict]) -> List[Dict]:
    """오늘 체크인 예약 조회"""
    today = date.today()
    today_str = today.strftime('%Y-%m-%d')
    
    checkins = []
    for res in reservations:
        check_in = res.get('check_in', '')
        if str(check_in) == today_str and res.get('status') in ['confirmed', 'checked_in']:
            checkins.append(res)
    
    return checkins


def get_today_checkouts(reservations: List[Dict]) -> List[Dict]:
    """오늘 체크아웃 예약 조회"""
    today = date.today()
    today_str = today.strftime('%Y-%m-%d')
    
    checkouts = []
    for res in reservations:
        check_out = res.get('check_out', '')
        if str(check_out) == today_str and res.get('status') in ['confirmed', 'checked_in']:
            checkouts.append(res)
    
    return checkouts


def reservation_dict_to_model(res_dict: Dict) -> Reservation:
    """딕셔너리를 Reservation 모델로 변환"""
    # status가 비어있으면 기본값 설정
    status = res_dict.get('status', '').strip()
    if not status:
        status = 'Reserved'
    
    # Status 값 정규화 (기존 값들을 새 형식으로 변환)
    status_map = {
        'confirmed': 'Reserved',
        'Not Checked': 'Reserved',
        'checked_in': 'Checked in',
        'checked_out': 'Checked out',
        'cancelled': 'Reserved'
    }
    if status in status_map:
        status = status_map[status]
    
    # booking_reference가 비어있으면 기본값 설정
    booking_ref = res_dict.get('booking_reference', '').strip()
    if not booking_ref:
        booking_ref = f"REF-{res_dict.get('id', 'N/A')}"
    
    return Reservation(
        id=res_dict.get('id'),
        customer_id=res_dict.get('customer_id', ''),
        room_id=res_dict.get('room_id', ''),
        platform_id=res_dict.get('platform_id', ''),
        check_in=parse_date(res_dict.get('check_in', '')),
        check_out=parse_date(res_dict.get('check_out', '')),
        guests=int(res_dict.get('guests', 0)) if res_dict.get('guests') else 0,
        total_price=float(res_dict.get('total_price', 0)) if res_dict.get('total_price') else 0.0,
        status=status,
        booking_reference=booking_ref,
        notes=res_dict.get('notes', '').strip() if res_dict.get('notes') else None,
        created_at=res_dict.get('created_at')
    )

