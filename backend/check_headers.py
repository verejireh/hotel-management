"""
시트의 헤더 확인 스크립트
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.sheets import GoogleSheetsDB

def check_headers():
    """각 시트의 헤더 확인"""
    print("Checking sheet headers...")
    print("=" * 50)
    
    try:
        db = GoogleSheetsDB()
        
        sheets_to_check = {
            "customers": ["id", "name", "email", "phone", "nationality"],
            "reservation": ["id", "customer_id", "room_id", "platform_id", "check_in", "check_out", "guests", "total_price", "status", "booking_reference", "notes", "created_at"],
            "booking_platforms": ["id", "name", "api_key", "webhook_url"],
            "rooms": ["id", "room_number", "room_type", "max_guests", "price_per_night", "status"]
        }
        
        for sheet_name, expected_headers in sheets_to_check.items():
            print(f"\n[{sheet_name}]")
            try:
                data = db._read_sheet(sheet_name)
                if len(data) == 0:
                    print("  [ERROR] Sheet is completely empty")
                elif len(data) == 1:
                    headers = data[0]
                    print(f"  Headers found: {headers}")
                    print(f"  Expected: {expected_headers}")
                    
                    # 헤더 비교
                    if headers == expected_headers:
                        print("  [OK] Headers match perfectly!")
                    else:
                        print("  [WARNING] Headers don't match exactly")
                        missing = set(expected_headers) - set(headers)
                        extra = set(headers) - set(expected_headers)
                        if missing:
                            print(f"    Missing: {missing}")
                        if extra:
                            print(f"    Extra: {extra}")
                else:
                    headers = data[0]
                    row_count = len(data) - 1
                    print(f"  Headers: {headers}")
                    print(f"  Data rows: {row_count}")
                    if row_count > 0:
                        print(f"  First data row: {data[1]}")
            except Exception as e:
                print(f"  [ERROR] {e}")
        
        print("\n" + "=" * 50)
        print("Header check completed!")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = check_headers()
    sys.exit(0 if success else 1)







