# 관리자 및 룸 메모 기능 가이드

## 새로 추가된 기능

### 1. 관리자 관리
- **위치**: `/admins`
- **기능**:
  - 관리자 목록 조회
  - 새 관리자 추가
  - 관리자 정보 관리 (이름, 이메일, 전화번호, 역할, 활성 상태)

### 2. 룸 메모 작성
- **위치**: `/rooms` (각 방 카드의 "Add Note" 버튼)
- **기능**:
  - 각 방에 대한 메모 작성
  - 메모 타입 선택:
    - **Urgent**: 긴급한 사항 (즉시 처리 필요)
    - **After Checkout**: 체크아웃 후 처리 사항

### 3. 알람 시스템
- **위치**: `/` (Dashboard)
- **기능**:
  - 긴급 메모 알람 표시
  - 체크아웃 후 작업 알람 표시
  - 알람 완료 처리

## Google Sheets 설정

다음 2개의 시트를 Google Sheets에 추가해야 합니다:

### 1. admins 시트
컬럼명 (첫 번째 행):
- id
- name
- email
- phone
- role
- is_active

### 2. room_notes 시트
컬럼명 (첫 번째 행):
- id
- room_id
- admin_id
- note_type (urgent 또는 after_checkout)
- title
- description
- status (pending 또는 completed)
- created_at
- completed_at
- reservation_id

## 시트 생성 방법

1. Google Sheets를 열고 하단의 "+" 버튼을 클릭하여 새 시트 추가
2. 시트 이름을 `admins`로 변경
3. 첫 번째 행에 위의 컬럼명 입력
4. 다시 "+" 버튼을 클릭하여 새 시트 추가
5. 시트 이름을 `room_notes`로 변경
6. 첫 번째 행에 위의 컬럼명 입력

또는 다음 스크립트를 실행하여 자동으로 헤더를 생성할 수 있습니다:

```bash
cd backend
python setup_admins_notes.py
```

(시트가 이미 생성되어 있어야 합니다)

## API 엔드포인트

### 관리자 관련
- `GET /api/admins/` - 모든 관리자 조회
- `GET /api/admins/{id}` - 관리자 상세 조회
- `POST /api/admins/` - 새 관리자 생성

### 룸 메모 관련
- `GET /api/room-notes/` - 모든 룸 메모 조회 (room_id 필터 옵션)
- `GET /api/room-notes/urgent` - 긴급 메모 조회
- `GET /api/room-notes/after-checkout` - 체크아웃 후 메모 조회
- `GET /api/room-notes/alerts` - 모든 알람 조회
- `POST /api/room-notes/` - 새 룸 메모 생성
- `POST /api/room-notes/{note_id}/complete` - 메모 완료 처리

## 사용 방법

### 1. 관리자 추가
1. "Admins" 메뉴 클릭
2. "+ New Admin" 버튼 클릭
3. 관리자 정보 입력 후 저장

### 2. 룸 메모 작성
1. "Rooms" 메뉴 클릭
2. 방 카드에서 "Add Note" 버튼 클릭
3. 메모 타입 선택:
   - **Urgent**: 즉시 처리해야 하는 긴급 사항
   - **After Checkout**: 체크아웃 후 처리할 사항
4. 제목과 설명 입력
5. 담당 관리자 선택
6. 저장

### 3. 알람 확인 및 처리
1. Dashboard에서 알람 확인
2. 긴급 알람은 빨간색으로 표시
3. 체크아웃 후 작업은 초록색으로 표시
4. "Complete" 버튼으로 완료 처리

## 알람 동작 방식

- **긴급 메모 (Urgent)**: 생성 즉시 Dashboard에 알람으로 표시
- **체크아웃 후 메모 (After Checkout)**: 체크아웃이 완료된 후 Dashboard에 알람으로 표시
- 완료 처리된 메모는 알람에서 자동으로 제거됨







