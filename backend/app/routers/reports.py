from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, StreamingResponse
from datetime import date, datetime
from app.db import MySQLDB
from app.utils import reservation_dict_to_model
import io
import csv

router = APIRouter(prefix="/api/reports", tags=["reports"])


def get_db():
    return MySQLDB()


@router.get("/reservations/excel")
async def export_reservations_excel(start_date: str = None, end_date: str = None, db: MySQLDB = Depends(get_db)):
    """예약 리포트 Excel 다운로드"""
    try:
        import openpyxl
        from openpyxl import Workbook
        from app.utils import parse_date
        
        reservations_data = db.get_reservations()
        
        # 날짜 필터링
        if start_date and end_date:
            start = parse_date(start_date)
            end = parse_date(end_date)
            filtered_reservations = []
            for res_data in reservations_data:
                try:
                    check_in = parse_date(res_data.get('check_in', ''))
                    if start <= check_in <= end:
                        filtered_reservations.append(res_data)
                except:
                    continue
            reservations_data = filtered_reservations
        
        # Excel 워크북 생성
        wb = Workbook()
        ws = wb.active
        ws.title = "Reservations"
        
        # 헤더
        headers = ["ID", "Customer ID", "Room ID", "Platform", "Check-in", "Check-out", 
                  "Guests", "Total Price", "Status", "Booking Reference", "Notes"]
        ws.append(headers)
        
        # 데이터
        platforms_data = db.get_platforms()
        platform_map = {p.get('id', ''): p.get('name', 'Unknown') for p in platforms_data}
        
        for res_data in reservations_data:
            platform_id = res_data.get('platform_id', '')
            platform_name = platform_map.get(platform_id, f"Platform {platform_id}")
            
            row = [
                res_data.get('id', ''),
                res_data.get('customer_id', ''),
                res_data.get('room_id', ''),
                platform_name,
                res_data.get('check_in', ''),
                res_data.get('check_out', ''),
                res_data.get('guests', ''),
                res_data.get('total_price', ''),
                res_data.get('status', ''),
                res_data.get('booking_reference', ''),
                res_data.get('notes', '')
            ]
            ws.append(row)
        
        # 파일로 저장
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        filename = f"reservations_{date.today().strftime('%Y%m%d')}.xlsx"
        
        return StreamingResponse(
            io.BytesIO(output.read()),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except ImportError:
        # openpyxl이 없으면 CSV로 대체
        return await export_reservations_csv(start_date, end_date, db)


@router.get("/reservations/csv")
async def export_reservations_csv(start_date: str = None, end_date: str = None, db: MySQLDB = Depends(get_db)):
    """예약 리포트 CSV 다운로드"""
    from app.utils import parse_date
    
    reservations_data = db.get_reservations()
    
    # 날짜 필터링
    if start_date and end_date:
        start = parse_date(start_date)
        end = parse_date(end_date)
        filtered_reservations = []
        for res_data in reservations_data:
            try:
                check_in = parse_date(res_data.get('check_in', ''))
                if start <= check_in <= end:
                    filtered_reservations.append(res_data)
            except:
                continue
        reservations_data = filtered_reservations
    
    # CSV 생성
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 헤더
    writer.writerow(["ID", "Customer ID", "Room ID", "Platform", "Check-in", "Check-out", 
                     "Guests", "Total Price", "Status", "Booking Reference", "Notes"])
    
    # 데이터
    platforms_data = db.get_platforms()
    platform_map = {p.get('id', ''): p.get('name', 'Unknown') for p in platforms_data}
    
    for res_data in reservations_data:
        platform_id = res_data.get('platform_id', '')
        platform_name = platform_map.get(platform_id, f"Platform {platform_id}")
        
        writer.writerow([
            res_data.get('id', ''),
            res_data.get('customer_id', ''),
            res_data.get('room_id', ''),
            platform_name,
            res_data.get('check_in', ''),
            res_data.get('check_out', ''),
            res_data.get('guests', ''),
            res_data.get('total_price', ''),
            res_data.get('status', ''),
            res_data.get('booking_reference', ''),
            res_data.get('notes', '')
        ])
    
    output.seek(0)
    filename = f"reservations_{date.today().strftime('%Y%m%d')}.csv"
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )






