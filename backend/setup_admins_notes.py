"""
admins와 room_notes 시트에 헤더 자동 생성 스크립트
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.sheets import GoogleSheetsDB

def setup_sheets():
    """시트에 헤더 자동 생성"""
    print("Setting up admins and room_notes sheets...")
    print("=" * 50)
    
    try:
        db = GoogleSheetsDB()
        
        # admin 시트 헤더
        print("\n[admin]")
        try:
            data = db._read_sheet("admin")
            if len(data) == 0:
                headers = ["Name", "Email", "Phone", "Role"]
                db._write_sheet("admin", [headers], "A1")
                print(f"  [OK] Headers added: {headers}")
            else:
                print(f"  [OK] Headers already exist: {data[0]}")
        except Exception as e:
            print(f"  [ERROR] {e}")
        
        # room_notes 시트 헤더
        print("\n[room_notes]")
        try:
            data = db._read_sheet("room_notes")
            if len(data) == 0:
                headers = [
                    "id", "room_id", "admin_id", "note_type", "title",
                    "description", "status", "created_at", "completed_at", "reservation_id"
                ]
                db._write_sheet("room_notes", [headers], "A1")
                print(f"  [OK] Headers added: {headers}")
            else:
                print(f"  [OK] Headers already exist: {data[0]}")
        except Exception as e:
            print(f"  [ERROR] {e}")
        
        print("\n" + "=" * 50)
        print("Setup completed!")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = setup_sheets()
    sys.exit(0 if success else 1)

