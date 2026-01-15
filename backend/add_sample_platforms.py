"""
booking_platforms 시트에 샘플 데이터 추가 스크립트
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.sheets import GoogleSheetsDB

def add_sample_platforms():
    """booking_platforms 시트에 샘플 플랫폼 데이터 추가"""
    print("Adding sample booking platforms...")
    print("=" * 50)
    
    try:
        db = GoogleSheetsDB()
        
        # 샘플 플랫폼 데이터
        platforms = [
            ["1", "Airbnb", "", ""],
            ["2", "Agoda", "", ""],
            ["3", "Hotels.com", "", ""],
            ["4", "Rakuten Travel", "", ""],
            ["5", "Booking.com", "", ""],
            ["6", "Expedia", "", ""],
        ]
        
        # 현재 데이터 확인
        current_data = db._read_sheet("booking_platforms")
        
        if len(current_data) <= 1:  # 헤더만 있거나 비어있음
            print("\nAdding sample platforms...")
            for platform in platforms:
                db._append_to_sheet("booking_platforms", [platform])
                print(f"  Added: {platform[1]} (ID: {platform[0]})")
        else:
            print(f"\n[INFO] booking_platforms already has {len(current_data) - 1} row(s)")
            print("Current platforms:")
            for row in current_data[1:]:
                if row:
                    print(f"  ID: {row[0]}, Name: {row[1] if len(row) > 1 else 'N/A'}")
            
            response = input("\nAdd sample platforms anyway? (y/n): ")
            if response.lower() == 'y':
                for platform in platforms:
                    db._append_to_sheet("booking_platforms", [platform])
                    print(f"  Added: {platform[1]} (ID: {platform[0]})")
        
        # 최종 확인
        print("\n" + "=" * 50)
        print("Final booking_platforms data:")
        final_data = db._read_sheet("booking_platforms")
        if len(final_data) > 1:
            for row in final_data[1:]:
                if row:
                    print(f"  ID: {row[0]}, Name: {row[1] if len(row) > 1 else 'N/A'}")
        else:
            print("  No platforms found")
        
        print("\nSetup completed!")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = add_sample_platforms()
    sys.exit(0 if success else 1)







