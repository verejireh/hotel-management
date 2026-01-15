# Quick Start Guide

## 1. Google Sheets 설정 확인

### 시트 ID 설정

시트 ID를 설정하는 방법은 두 가지가 있습니다:

#### 방법 1: .env 파일 사용 (권장)
`backend` 폴더에 `.env` 파일을 생성하고 다음을 추가:

```
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
```

#### 방법 2: 코드에 직접 입력
`backend/app/sheets.py` 파일의 13번째 줄을 수정:

```python
google_sheets_spreadsheet_id: str = "your_spreadsheet_id_here"
```

### 시트 구조 확인

Google Sheets에 다음 4개의 시트가 있어야 합니다:

1. **customers** - 고객 정보
2. **reservation** - 예약 정보  
3. **booking_platforms** - 예약 플랫폼 정보
4. **Rooms** - 객실 정보

각 시트의 첫 번째 행에는 컬럼명(헤더)이 있어야 합니다.
자세한 내용은 `SHEETS_SETUP.md`를 참조하세요.

## 2. 연결 테스트

```bash
cd backend
python test_connection.py
```

성공하면 각 시트의 헤더 정보가 표시됩니다.

## 3. 백엔드 서버 실행

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

서버가 실행되면:
- API 문서: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## 4. 프론트엔드 실행

새 터미널에서:

```bash
cd frontend
npm install
npm run dev
```

브라우저에서 http://localhost:5173 접속

## 문제 해결

### 시트를 찾을 수 없다는 에러가 나는 경우

1. 시트 ID가 올바른지 확인
2. Google Sheets에서 서비스 계정 이메일을 공유했는지 확인
   - credentials.json 파일에 있는 `client_email` 값을 확인
   - Google Sheets에서 해당 이메일 주소에 편집 권한 부여

### 404 에러가 나는 경우

- 시트 이름이 정확한지 확인 (대소문자 구분)
- 각 시트의 첫 번째 행에 헤더가 있는지 확인







