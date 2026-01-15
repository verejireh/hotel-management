# 호텔 관리 시스템

여러 예약 플랫폼(Airbnb, Agoda, Hotels.com, Rakuten 등)의 예약을 중복 없이 통합 관리하는 호텔 관리자 페이지입니다.

## 주요 기능

- ✅ **중복 예약 방지**: 여러 플랫폼의 예약을 자동으로 중복 체크
- 📅 **체크인/체크아웃 관리**: 오늘의 체크인/체크아웃 명부를 한눈에 확인
- 🏨 **예약 관리**: 모든 예약을 통합하여 관리
- 🛏️ **객실 관리**: 객실 상태 및 정보 관리
- 📊 **대시보드**: 실시간 통계 및 현황 확인

## 기술 스택

- **백엔드**: FastAPI (Python)
- **프론트엔드**: Vue 3 + Vite
- **데이터베이스**: Google Sheets

## 프로젝트 구조

```
elimwood/
├── backend/          # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py          # FastAPI 앱 진입점
│   │   ├── models.py         # Pydantic 모델
│   │   ├── sheets.py         # Google Sheets 연동
│   │   ├── utils.py          # 유틸리티 함수
│   │   └── routers/          # API 라우터
│   │       ├── reservations.py
│   │       ├── rooms.py
│   │       └── dashboard.py
│   └── requirements.txt
├── frontend/         # Vue 프론트엔드
│   ├── src/
│   │   ├── views/           # 페이지 컴포넌트
│   │   ├── components/      # 재사용 컴포넌트
│   │   ├── services/        # API 서비스
│   │   └── router/          # Vue Router
│   └── package.json
└── README.md
```

## 설치 및 실행

### 1. Google Sheets 설정

1. Google Cloud Console에서 프로젝트 생성
2. Google Sheets API 활성화
3. 서비스 계정 생성 및 JSON 키 다운로드
4. 다운로드한 JSON 파일을 `backend/credentials.json`으로 저장
5. Google Sheets에 다음 시트 생성:
   - `customers` (id, name, email, phone, nationality)
   - `reservation` (id, customer_id, room_id, platform_id, check_in, check_out, guests, total_price, status, booking_reference, notes, created_at)
   - `booking_platforms` (id, name, api_key, webhook_url)
   - `Rooms` (id, room_number, room_type, max_guests, price_per_night, status)

6. 생성한 Google Sheets의 ID를 `.env` 파일에 설정

### 2. 백엔드 설정

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

`.env` 파일 생성:
```
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
CORS_ORIGINS=http://localhost:5173
```

백엔드 실행:
```bash
uvicorn app.main:app --reload --port 8000
```

### 3. 프론트엔드 설정

```bash
cd frontend
npm install
npm run dev
```

## API 엔드포인트

### 예약 관리
- `GET /api/reservations/` - 모든 예약 조회
- `GET /api/reservations/{id}` - 예약 상세 조회
- `POST /api/reservations/` - 새 예약 생성 (중복 체크 포함)
- `GET /api/reservations/room/{room_id}/availability` - 방 가용성 체크

### 객실 관리
- `GET /api/rooms/` - 모든 방 조회
- `GET /api/rooms/{id}` - 방 상세 조회

### 대시보드
- `GET /api/dashboard/checkin-out` - 오늘의 체크인/체크아웃 명부
- `GET /api/dashboard/stats` - 대시보드 통계

## 추가 기능 제안

1. **예약 캘린더 뷰**: 월별/주별로 예약 현황을 캘린더 형식으로 표시
2. **수익 분석**: 일별/월별 수익 통계 및 그래프
3. **고객 관리**: 고객 정보 상세 관리 및 이력 조회
4. **알림 시스템**: 체크인/체크아웃 예정 알림
5. **리포트 생성**: 예약 리포트 PDF/Excel 다운로드
6. **플랫폼별 통계**: 각 예약 플랫폼별 예약 현황 및 수익 분석
7. **방 청소 관리**: 청소 상태 및 청소 일정 관리
8. **체크인/체크아웃 프로세스**: 실제 체크인/체크아웃 처리 기능

## 라이선스

MIT







# hotel-management
# hotel-management
