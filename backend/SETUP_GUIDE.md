# MySQL 설정 가이드 (단계별 설명)

## 사용자가 직접 해야 하는 작업

### 1. MySQL 설치 (직접 설치 필요)
- Windows: MySQL 공식 사이트에서 설치 프로그램 다운로드 및 설치
- macOS: `brew install mysql` 또는 공식 설치 프로그램
- Linux: `sudo apt-get install mysql-server` 등

### 2. MySQL 서버 시작 (직접 실행 필요)
- Windows: MySQL 서비스가 자동으로 시작됨 (설치 시 설정)
- macOS: `brew services start mysql`
- Linux: `sudo systemctl start mysql`

### 3. MySQL에 접속하여 데이터베이스 생성 (직접 실행 필요)
MySQL 명령줄 또는 MySQL Workbench 등으로 접속:

```bash
mysql -u root -p
```

접속 후 다음 명령어 실행:

```sql
CREATE DATABASE hotel_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**이 작업은 반드시 직접 해야 합니다!** (프로그램이 자동으로 하지 않습니다)

### 4. 환경 변수 설정 (직접 편집 필요)
`backend/.env` 파일을 생성하거나 편집:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=hotel_management
```

**이 작업도 직접 해야 합니다!**

### 5. 필요한 패키지 설치 (터미널에서 실행)
```bash
cd backend
pip install -r requirements.txt
```

**터미널에서 직접 실행해야 합니다!**

---

## 자동으로 실행되는 작업 (스크립트 실행)

### 6. 데이터베이스 테이블 생성 (스크립트 실행)
```bash
python init_db.py
```

이 스크립트를 실행하면 **자동으로** 다음 테이블들이 생성됩니다:
- customers
- rooms
- booking_platforms
- reservations
- admins
- room_notes

**이 작업은 스크립트가 자동으로 합니다!** (MySQL에 접속할 필요 없음)

### 7. 데이터 마이그레이션 (선택사항, 스크립트 실행)
```bash
python migrate_from_sheets.py
```

기존 Google Sheets 데이터를 MySQL로 옮기려면 이 스크립트를 실행합니다.

**이 작업도 스크립트가 자동으로 합니다!**

---

## 요약

### 직접 해야 하는 작업:
1. ✅ MySQL 설치
2. ✅ MySQL 서버 시작
3. ✅ MySQL 접속하여 데이터베이스 생성 (`CREATE DATABASE ...`)
4. ✅ `.env` 파일 편집 (MySQL 비밀번호 등)
5. ✅ `pip install -r requirements.txt` 실행

### 자동으로 되는 작업:
- ❌ 데이터베이스 테이블 생성 → `python init_db.py` 실행하면 자동
- ❌ 데이터 마이그레이션 → `python migrate_from_sheets.py` 실행하면 자동

---

## 빠른 시작 (순서대로)

1. **MySQL 설치 및 시작**
2. **MySQL 접속하여 데이터베이스 생성:**
   ```sql
   CREATE DATABASE hotel_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. **`.env` 파일 생성/편집:**
   ```env
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=hotel_management
   ```
4. **패키지 설치:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
5. **테이블 생성 (자동):**
   ```bash
   python init_db.py
   ```
6. **서버 실행:**
   ```bash
   python -m uvicorn app.main:app --reload --port 8000
   ```


