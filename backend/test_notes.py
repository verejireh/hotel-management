"""
note 시트 읽기 테스트 스크립트
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.sheets import GoogleSheetsDB

def test_read_notes():
    """note 시트 읽기 테스트"""
    print("=" * 50)
    print("Testing note sheet reading...")
    print("=" * 50)
    
    try:
        db = GoogleSheetsDB()
        
        # note 시트 읽기
        print("\n[note 시트 읽기]")
        data = db._read_sheet("note")
        print(f"읽은 행 수: {len(data)}")
        
        if len(data) == 0:
            print("  [ERROR] 시트가 비어있습니다!")
            return
        
        # 헤더 확인
        headers = data[0]
        print(f"\n헤더: {headers}")
        print(f"헤더 개수: {len(headers)}")
        
        # 데이터 행 확인
        if len(data) < 2:
            print("\n  [WARNING] 헤더만 있고 데이터 행이 없습니다!")
        else:
            print(f"\n데이터 행 개수: {len(data) - 1}")
            for i, row in enumerate(data[1:6], start=2):  # 처음 5개 행만
                print(f"\n  행 {i}:")
                for j, (header, value) in enumerate(zip(headers, row)):
                    if j < len(row):
                        print(f"    {header}: '{row[j]}'")
                    else:
                        print(f"    {header}: (없음)")
        
        # get_notes() 메서드 테스트
        print("\n" + "=" * 50)
        print("[get_notes() 메서드 테스트]")
        print("=" * 50)
        
        notes = db.get_notes()
        print(f"\n반환된 노트 개수: {len(notes)}")
        
        if len(notes) > 0:
            print("\n첫 번째 노트:")
            first_note = notes[0]
            for key, value in first_note.items():
                print(f"  {key}: {value}")
        else:
            print("\n  [WARNING] 노트가 없습니다!")
            if len(data) >= 2:
                print("\n  원본 데이터는 있지만 노트로 변환되지 않았습니다.")
                print("  가능한 원인:")
                print("    1. title과 description이 모두 비어있음")
                print("    2. 헤더 매핑이 잘못됨")
        
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
    success = test_read_notes()




