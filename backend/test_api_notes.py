"""
API 엔드포인트 직접 테스트
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.routers.room_notes import get_room_notes
from app.sheets import GoogleSheetsDB

async def test_api_endpoint():
    """API 엔드포인트 직접 테스트"""
    print("=" * 50)
    print("Testing API endpoint directly...")
    print("=" * 50)
    
    try:
        db = GoogleSheetsDB()
        
        # get_room_notes 함수 직접 호출
        print("\n[get_room_notes 호출]")
        result = await get_room_notes(room_id=None, progress=None, db=db)
        
        print(f"\n반환된 노트 개수: {len(result)}")
        if len(result) > 0:
            print("\n첫 번째 노트:")
            first_note = result[0]
            print(f"  id: {first_note.id}")
            print(f"  room_id: {first_note.room_id}")
            print(f"  title: {first_note.title}")
            print(f"  description: {first_note.description}")
        else:
            print("\n  [WARNING] 노트가 없습니다!")
        
        print("\n" + "=" * 50)
        print("테스트 완료!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(test_api_endpoint())

