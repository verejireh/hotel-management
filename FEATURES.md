# 호텔 관리 시스템 - 추가 기능 가이드

## 구현된 모든 기능

### ✅ 1. 예약 캘린더 뷰
- **위치**: `/calendar`
- **기능**:
  - 월별 예약 현황을 캘린더 형식으로 표시
  - 주별/일별 예약 확인
  - 예약 상태별 색상 구분
- **API**: 
  - `GET /api/calendar/month/{year}/{month}` - 월별 예약
  - `GET /api/calendar/week/{year}/{week}` - 주별 예약

### ✅ 2. 수익 분석
- **위치**: `/revenue`
- **기능**:
  - 일별 수익 통계 및 차트
  - 월별 수익 통계
  - 플랫폼별 수익 분석
  - Excel 리포트 다운로드
- **API**:
  - `GET /api/revenue/daily/{start_date}/{end_date}` - 일별 수익
  - `GET /api/revenue/monthly/{year}` - 월별 수익
  - `GET /api/revenue/platform/{start_date}/{end_date}` - 플랫폼별 수익

### ✅ 3. 고객 관리
- **위치**: `/customers`
- **기능**:
  - 고객 목록 조회
  - 고객 상세 정보 확인
  - 고객별 예약 이력 조회
  - 새 고객 추가
- **API**:
  - `GET /api/customers/` - 모든 고객
  - `GET /api/customers/{id}` - 고객 상세
  - `GET /api/customers/{id}/reservations` - 고객 예약 이력
  - `POST /api/customers/` - 새 고객 생성

### ✅ 4. 체크인/체크아웃 프로세스
- **위치**: `/reservations` (각 예약 카드에 버튼)
- **기능**:
  - 예약 상태를 "checked_in"으로 변경
  - 예약 상태를 "checked_out"으로 변경
  - 체크아웃 시 방 상태를 "cleaning"으로 자동 변경
- **API**:
  - `POST /api/checkinout/checkin/{reservation_id}` - 체크인
  - `POST /api/checkinout/checkout/{reservation_id}` - 체크아웃
  - `GET /api/checkinout/upcoming?days=7` - 다가오는 체크인/체크아웃

### ✅ 5. 플랫폼별 통계
- **위치**: `/revenue` (플랫폼별 수익 차트)
- **기능**:
  - 각 예약 플랫폼별 수익 통계
  - 플랫폼별 예약 건수
  - 시각적 차트 표시
- **API**: `GET /api/revenue/platform/{start_date}/{end_date}`

### ✅ 6. 방 청소 관리
- **위치**: `/cleaning`
- **기능**:
  - 청소가 필요한 방 목록 표시
  - 청소 완료 처리
  - 청소 완료 시 방 상태를 "available"로 변경
- **API**:
  - `GET /api/cleaning/rooms` - 청소 필요한 방 목록
  - `POST /api/cleaning/complete/{room_id}` - 청소 완료

### ✅ 7. 알림 시스템
- **위치**: `/` (Dashboard)
- **기능**:
  - 다가오는 체크인/체크아웃 알림 표시
  - 7일 이내 예정된 체크인/체크아웃 자동 표시
  - 날짜순 정렬
- **API**: `GET /api/checkinout/upcoming?days=7`

### ✅ 8. 리포트 생성
- **위치**: `/revenue` (Export Excel 버튼)
- **기능**:
  - 예약 리포트 Excel 다운로드
  - 예약 리포트 CSV 다운로드
  - 날짜 범위 필터링 지원
- **API**:
  - `GET /api/reports/reservations/excel?start_date=&end_date=` - Excel 다운로드
  - `GET /api/reports/reservations/csv?start_date=&end_date=` - CSV 다운로드

## 사용 방법

### 의존성 설치

**백엔드**:
```bash
cd backend
pip install -r requirements.txt
```

**프론트엔드**:
```bash
cd frontend
npm install
```

### 서버 실행

**백엔드**:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**프론트엔드**:
```bash
cd frontend
npm run dev
```

### 접속

- 프론트엔드: http://localhost:5173
- API 문서: http://localhost:8000/docs

## 주요 기능 사용 가이드

### 1. 예약 캘린더 사용
1. "Calendar" 메뉴 클릭
2. 월별 예약 현황 확인
3. Previous/Next 버튼으로 월 이동

### 2. 수익 분석 사용
1. "Revenue" 메뉴 클릭
2. 날짜 범위 선택
3. "Apply" 버튼 클릭
4. 차트 및 통계 확인
5. "Export Excel" 버튼으로 리포트 다운로드

### 3. 고객 관리 사용
1. "Customers" 메뉴 클릭
2. 고객 카드 클릭하여 상세 정보 및 예약 이력 확인
3. "+ New Customer" 버튼으로 새 고객 추가

### 4. 체크인/체크아웃 사용
1. "Reservations" 메뉴 클릭
2. 예약 카드에서 "Check In" 또는 "Check Out" 버튼 클릭
3. 확인 후 상태 업데이트

### 5. 청소 관리 사용
1. "Cleaning" 메뉴 클릭
2. 청소가 필요한 방 목록 확인
3. "Mark as Cleaned" 버튼으로 청소 완료 처리

## API 엔드포인트 전체 목록

### 예약 관리
- `GET /api/reservations/` - 모든 예약
- `GET /api/reservations/{id}` - 예약 상세
- `POST /api/reservations/` - 새 예약 생성
- `GET /api/reservations/room/{room_id}/availability` - 방 가용성 체크

### 객실 관리
- `GET /api/rooms/` - 모든 방
- `GET /api/rooms/{id}` - 방 상세

### 대시보드
- `GET /api/dashboard/checkin-out` - 오늘의 체크인/체크아웃
- `GET /api/dashboard/stats` - 대시보드 통계

### 캘린더
- `GET /api/calendar/month/{year}/{month}` - 월별 예약
- `GET /api/calendar/week/{year}/{week}` - 주별 예약

### 수익 분석
- `GET /api/revenue/daily/{start_date}/{end_date}` - 일별 수익
- `GET /api/revenue/monthly/{year}` - 월별 수익
- `GET /api/revenue/platform/{start_date}/{end_date}` - 플랫폼별 수익

### 고객 관리
- `GET /api/customers/` - 모든 고객
- `GET /api/customers/{id}` - 고객 상세
- `GET /api/customers/{id}/reservations` - 고객 예약 이력
- `POST /api/customers/` - 새 고객 생성

### 체크인/체크아웃
- `POST /api/checkinout/checkin/{reservation_id}` - 체크인
- `POST /api/checkinout/checkout/{reservation_id}` - 체크아웃
- `GET /api/checkinout/upcoming?days=7` - 다가오는 체크인/체크아웃

### 청소 관리
- `GET /api/cleaning/rooms` - 청소 필요한 방 목록
- `POST /api/cleaning/complete/{room_id}` - 청소 완료

### 리포트
- `GET /api/reports/reservations/excel` - Excel 리포트
- `GET /api/reports/reservations/csv` - CSV 리포트







