"""
Google Sheets 연결 테스트 스크립트
"""
import sys
import os

# app 모듈을 import하기 위해 경로 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.sheets import GoogleSheetsDB

def test_connection():
    """Google Sheets 연결 및 기본 테스트"""
    print("Testing Google Sheets connection...")
    print("=" * 50)
    
    # 시트 ID 확인
    from app.sheets import settings
    if not settings.google_sheets_spreadsheet_id:
        print("\n[ERROR] Google Sheets Spreadsheet ID is not set!")
        print("\nPlease set it in one of the following ways:")
        print("1. Create a .env file in the backend folder with:")
        print("   GOOGLE_SHEETS_SPREADSHEET_ID=your_sheet_id_here")
        print("\n2. Or edit backend/app/sheets.py and set:")
        print("   google_sheets_spreadsheet_id: str = \"your_sheet_id_here\"")
        return False
    
    print(f"Spreadsheet ID: {settings.google_sheets_spreadsheet_id}")
    print()
    
    try:
        # Google Sheets DB 인스턴스 생성
        db = GoogleSheetsDB()
        print("[OK] Google Sheets service initialized successfully")
        
        # 각 시트 존재 확인
        sheets_to_check = ["customers", "reservation", "booking_platforms", "rooms"]
        
        for sheet_name in sheets_to_check:
            try:
                data = db._read_sheet(sheet_name)
                if len(data) > 0:
                    headers = data[0]
                    print(f"\n[OK] Sheet '{sheet_name}' found")
                    print(f"  Headers: {headers}")
                    print(f"  Rows: {len(data) - 1} (excluding header)")
                else:
                    print(f"\n[WARNING] Sheet '{sheet_name}' exists but is empty")
            except Exception as e:
                print(f"\n[ERROR] Error reading sheet '{sheet_name}': {e}")
        
        print("\n" + "=" * 50)
        print("Connection test completed!")
        
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        print("Please make sure credentials.json is in the backend folder")
        return False
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("Please check your Google Sheets API setup and permissions")
        return False
    
    return True

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

