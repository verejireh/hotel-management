# MySQL 데이터베이스 설정 가이드

## 1. MySQL 설치

### Windows
1. MySQL 공식 사이트에서 MySQL 설치 프로그램 다운로드
2. 설치 시 root 비밀번호 설정
3. MySQL 서비스 시작

### macOS
```bash
brew install mysql
brew services start mysql
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo systemctl start mysql
```

## 2. 데이터베이스 생성

MySQL에 접속하여 데이터베이스를 생성합니다:

```sql
CREATE DATABASE hotel_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 3. 환경 변수 설정

`.env` 파일에 다음 설정을 추가하세요:

```env
# MySQL 설정
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=hotel_management
```

## 4. 필요한 패키지 설치

```bash
cd backend
pip install -r requirements.txt
```

## 5. 데이터베이스 테이블 생성

```bash
python init_db.py
```

이 명령어는 다음 테이블들을 생성합니다:
- `customers` - 고객 정보
- `rooms` - 객실 정보
- `booking_platforms` - 예약 플랫폼 정보
- `reservations` - 예약 정보
- `admins` - 관리자 정보
- `room_notes` - 객실 노트 정보

## 6. Google Sheets에서 데이터 마이그레이션 (선택사항)

기존 Google Sheets 데이터를 MySQL로 마이그레이션하려면:

```bash
python migrate_from_sheets.py
```

**주의**: 이 스크립트는 Google Sheets API 자격 증명이 필요합니다. 
마이그레이션 전에 `credentials.json` 파일이 있는지 확인하세요.

## 7. 서버 실행

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

## 문제 해결

### 연결 오류
- MySQL 서비스가 실행 중인지 확인
- `.env` 파일의 설정이 올바른지 확인
- 방화벽 설정 확인

### 인코딩 문제
- 데이터베이스가 `utf8mb4` 문자셋을 사용하는지 확인
- 연결 URL에 `charset=utf8mb4`가 포함되어 있는지 확인


