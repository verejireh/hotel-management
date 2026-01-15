# .env 파일 생성 가이드

## 문제
현재 원격 MySQL 서버(`34.146.155.206`)로 연결을 시도하고 있어 타임아웃이 발생합니다.

## 해결 방법

### 1. 로컬 MySQL을 사용하는 경우

`backend` 폴더에 `.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=여기에_MySQL_비밀번호_입력
MYSQL_DATABASE=hotel_management
```

**중요**: `MYSQL_PASSWORD`에 실제 MySQL root 비밀번호를 입력하세요!

### 2. 원격 MySQL을 사용하는 경우

원격 MySQL 서버를 사용하려면:
1. 서버가 실행 중인지 확인
2. 방화벽 설정 확인
3. 네트워크 연결 확인
4. `.env` 파일에 올바른 설정이 있는지 확인

### 3. .env 파일 생성 방법

#### Windows (메모장 사용)
1. `backend` 폴더로 이동
2. 메모장 열기
3. 위의 내용 입력
4. "다른 이름으로 저장" → 파일 이름: `.env` (확장자 없음)
5. 파일 형식: "모든 파일" 선택
6. 저장

#### VS Code 사용
1. `backend` 폴더에서 새 파일 생성
2. 파일 이름: `.env`
3. 위의 내용 입력
4. 저장

### 4. 설정 확인

`.env` 파일을 생성한 후 다음 명령어로 확인:

```bash
cd backend
python check_db_config.py
```

`MYSQL_HOST: localhost`로 표시되면 성공입니다!

### 5. 다음 단계

`.env` 파일을 생성한 후:

1. **MySQL 서버가 실행 중인지 확인**
2. **데이터베이스 생성** (아직 안 했다면):
   ```sql
   CREATE DATABASE hotel_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. **테이블 생성**:
   ```bash
   python init_db.py
   ```


