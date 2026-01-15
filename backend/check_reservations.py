"""
reservation 시트 데이터 확인 스크립트
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.sheets import GoogleSheetsDB

def check_reservations():
    """reservation 시트의 데이터 확인"""
    print("Checking reservation data...")
    print("=" * 50)
    
    try:
        db = GoogleSheetsDB()
        
        # 원시 데이터 읽기
        print("\n[Raw Data from Sheet]")
        raw_data = db._read_sheet("reservation")
        print(f"Total rows: {len(raw_data)}")
        
        if len(raw_data) == 0:
            print("  [ERROR] Sheet is completely empty")
            return False
        elif len(raw_data) == 1:
            print("  [WARNING] Only headers found, no data rows")
            print(f"  Headers: {raw_data[0]}")
        else:
            print(f"  Headers: {raw_data[0]}")
            print(f"  Data rows: {len(raw_data) - 1}")
            print("\n  Data rows:")
            for i, row in enumerate(raw_data[1:], start=2):
                print(f"    Row {i}: {row}")
                print(f"      Length: {len(row)}")
        
        # get_reservations() 메서드로 읽기
        print("\n[Using get_reservations() method]")
        reservations = db.get_reservations()
        print(f"Found {len(reservations)} reservations")
        
        for i, res in enumerate(reservations, 1):
            print(f"\n  Reservation {i}:")
            for key, value in res.items():
                print(f"    {key}: {value}")
        
        # 날짜 파싱 테스트
        print("\n[Date Parsing Test]")
        if reservations:
            first_res = reservations[0]
            check_in = first_res.get('check_in', '')
            check_out = first_res.get('check_out', '')
            print(f"  check_in (raw): {check_in} (type: {type(check_in)})")
            print(f"  check_out (raw): {check_out} (type: {type(check_out)})")
            
            # 날짜 형식 확인
            from app.utils import parse_date
            try:
                parsed_check_in = parse_date(check_in)
                print(f"  check_in (parsed): {parsed_check_in}")
            except Exception as e:
                print(f"  [ERROR] Failed to parse check_in: {e}")
            
            try:
                parsed_check_out = parse_date(check_out)
                print(f"  check_out (parsed): {parsed_check_out}")
            except Exception as e:
                print(f"  [ERROR] Failed to parse check_out: {e}")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = check_reservations()
    sys.exit(0 if success else 1)







