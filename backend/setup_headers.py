"""
시트에 헤더 자동 생성 스크립트
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.sheets import GoogleSheetsDB

def setup_headers():
    """각 시트에 헤더 자동 생성"""
    print("Setting up sheet headers...")
    print("=" * 50)
    
    try:
        db = GoogleSheetsDB()
        
        # 각 시트의 헤더 정의
        headers = {
            "customers": ["id", "name", "email", "phone", "nationality"],
            "reservation": ["id", "customer_id", "room_id", "platform_id", "check_in", "check_out", "guests", "total_price", "status", "booking_reference", "notes", "created_at"],
            "booking_platforms": ["id", "name", "api_key", "webhook_url"],
            "rooms": ["id", "room_number", "room_type", "max_guests", "price_per_night", "status"]
        }
        
        for sheet_name, header_row in headers.items():
            print(f"\n[{sheet_name}]")
            try:
                # 먼저 현재 데이터 확인
                current_data = db._read_sheet(sheet_name)
                
                if len(current_data) == 0:
                    # 빈 시트면 헤더 추가
                    print(f"  Sheet is empty, adding headers...")
                    db._write_sheet(sheet_name, [header_row], "A1")
                    print(f"  [OK] Headers added: {header_row}")
                elif len(current_data) == 1:
                    # 헤더만 있는 경우 확인
                    existing_headers = current_data[0]
                    if existing_headers == header_row:
                        print(f"  [OK] Headers already exist and match: {existing_headers}")
                    else:
                        print(f"  [WARNING] Headers exist but don't match")
                        print(f"    Existing: {existing_headers}")
                        print(f"    Expected: {header_row}")
                        # 사용자에게 물어볼 수도 있지만, 일단 덮어쓰기
                        response = input(f"  Overwrite headers? (y/n): ")
                        if response.lower() == 'y':
                            db._write_sheet(sheet_name, [header_row], "A1")
                            print(f"  [OK] Headers updated")
                else:
                    # 데이터가 있는 경우
                    existing_headers = current_data[0]
                    print(f"  [INFO] Sheet has data")
                    print(f"    Headers: {existing_headers}")
                    print(f"    Data rows: {len(current_data) - 1}")
                    if existing_headers != header_row:
                        print(f"    [WARNING] Headers don't match expected format")
                
            except Exception as e:
                print(f"  [ERROR] {e}")
                import traceback
                traceback.print_exc()
        
        print("\n" + "=" * 50)
        print("Header setup completed!")
        
        # 다시 확인
        print("\nVerifying headers...")
        for sheet_name in headers.keys():
            try:
                data = db._read_sheet(sheet_name)
                if len(data) > 0:
                    print(f"  [{sheet_name}] Headers: {data[0]}")
                else:
                    print(f"  [{sheet_name}] Still empty")
            except Exception as e:
                print(f"  [{sheet_name}] Error: {e}")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = setup_headers()
    sys.exit(0 if success else 1)







