# Google Sheets 설정 가이드

## 시트 구조

다음 4개의 시트가 필요합니다:

### 1. customers 시트
컬럼명 (첫 번째 행):
- id
- name
- email
- phone
- nationality

### 2. reservation 시트
컬럼명 (첫 번째 행):
- id
- customer_id
- room_id
- platform_id
- check_in
- check_out
- guests
- total_price
- status
- booking_reference
- notes
- created_at

### 3. booking_platforms 시트
컬럼명 (첫 번째 행):
- id
- name
- api_key
- webhook_url

### 4. rooms 시트
컬럼명 (첫 번째 행):
- id
- room_number
- room_type
- max_guests
- price_per_night
- status

## 중요 사항

1. **첫 번째 행은 반드시 컬럼명(헤더)이어야 합니다**
2. **시트 이름은 정확히 일치해야 합니다** (대소문자 구분)
   - `customers` (소문자)
   - `reservation` (소문자)
   - `booking_platforms` (소문자)
   - `rooms` (소문자)

## 연결 테스트

연결을 테스트하려면:

```bash
cd backend
python test_connection.py
```

이 스크립트는:
- Google Sheets API 연결 확인
- 각 시트 존재 여부 확인
- 시트의 헤더 정보 표시

## 환경 변수 설정

`.env` 파일에 다음을 추가하세요:

```
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
```

또는 `sheets.py` 파일의 `Settings` 클래스에서 직접 설정할 수 있습니다.

