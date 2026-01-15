"""
시트의 특정 셀 읽기 테스트
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.sheets import GoogleSheetsDB

def test_read_cells():
    """각 시트의 첫 번째 행 읽기 테스트"""
    print("Testing cell reading...")
    print("=" * 50)
    
    try:
        db = GoogleSheetsDB()
        
        sheets = ["customers", "reservation", "booking_platforms", "rooms"]
        
        for sheet_name in sheets:
            print(f"\n[{sheet_name}]")
            try:
                # A1 셀만 읽어보기
                result = db.service.spreadsheets().values().get(
                    spreadsheetId=db.spreadsheet_id,
                    range=f"{sheet_name}!A1:Z1"
                ).execute()
                
                values = result.get('values', [])
                if values and len(values) > 0:
                    print(f"  First row: {values[0]}")
                    print(f"  Number of columns: {len(values[0])}")
                else:
                    print("  [WARNING] No data in first row")
                    
                # 전체 데이터 읽기
                result2 = db.service.spreadsheets().values().get(
                    spreadsheetId=db.spreadsheet_id,
                    range=f"{sheet_name}!A:Z"
                ).execute()
                
                all_values = result2.get('values', [])
                print(f"  Total rows: {len(all_values)}")
                if len(all_values) > 0:
                    print(f"  First row: {all_values[0]}")
                    if len(all_values) > 1:
                        print(f"  Second row: {all_values[1]}")
                
            except Exception as e:
                print(f"  [ERROR] {e}")
        
        print("\n" + "=" * 50)
        print("Cell reading test completed!")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_read_cells()
    sys.exit(0 if success else 1)







