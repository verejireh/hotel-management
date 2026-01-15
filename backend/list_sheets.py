"""
Google Sheets에 있는 모든 시트 목록 확인
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.sheets import GoogleSheetsDB

def list_all_sheets():
    """시트에 있는 모든 탭(시트) 목록 확인"""
    print("Fetching all sheets from Google Spreadsheet...")
    print("=" * 50)
    
    try:
        db = GoogleSheetsDB()
        
        # 시트 메타데이터 가져오기
        spreadsheet = db.service.spreadsheets().get(
            spreadsheetId=db.spreadsheet_id
        ).execute()
        
        sheets = spreadsheet.get('sheets', [])
        
        if not sheets:
            print("No sheets found in the spreadsheet.")
            return
        
        print(f"\nFound {len(sheets)} sheet(s):\n")
        
        for i, sheet in enumerate(sheets, 1):
            sheet_title = sheet['properties']['title']
            sheet_id = sheet['properties']['sheetId']
            print(f"{i}. Sheet Name: '{sheet_title}' (ID: {sheet_id})")
        
        print("\n" + "=" * 50)
        print("\nRequired sheet names:")
        print("  - customers (lowercase)")
        print("  - reservation (lowercase)")
        print("  - booking_platforms (lowercase)")
        print("  - Rooms (capital R)")
        print("\nPlease make sure the sheet names match exactly (case-sensitive)!")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("\nPossible issues:")
        print("1. Spreadsheet ID is incorrect")
        print("2. Service account doesn't have access to the spreadsheet")
        print("   - Check the 'client_email' in credentials.json")
        print("   - Share the Google Sheet with that email address")
        return False
    
    return True

if __name__ == "__main__":
    success = list_all_sheets()
    sys.exit(0 if success else 1)







