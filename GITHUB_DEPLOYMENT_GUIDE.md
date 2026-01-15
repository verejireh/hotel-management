# GitHub 및 GCP 서버 배포 가이드

## 1단계: GitHub 저장소에 코드 Push

### 1.1 GitHub 저장소 생성

1. GitHub 웹사이트(https://github.com)에 로그인
2. 우측 상단의 **"+"** 버튼 클릭 → **"New repository"** 선택
3. 저장소 정보 입력:
   - **Repository name**: `elimwood` (또는 원하는 이름)
   - **Description**: (선택사항) "Hotel Management System"
   - **Public** 또는 **Private** 선택
   - **Initialize this repository with**: 체크하지 않음 (기존 코드가 있으므로)
4. **"Create repository"** 클릭

### 1.2 로컬에서 Git 초기화 및 Push

#### Windows (Git Bash 또는 PowerShell 사용)

```bash
# 프로젝트 루트 디렉토리로 이동
cd F:\myproject\elimwood

# Git 초기화 (이미 초기화되어 있으면 생략)
git init

# .gitignore 파일 생성 (중요!)
# .env 파일, __pycache__, node_modules 등은 커밋하지 않음
```

#### .gitignore 파일 생성

프로젝트 루트에 `.gitignore` 파일을 생성하고 다음 내용 추가:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# 환경 변수 (중요!)
.env
.env.local
.env.*.local

# Google Sheets 인증 정보
credentials.json
*.json

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Node.js (프론트엔드)
node_modules/
dist/
build/
*.log

# 데이터베이스
*.db
*.sqlite

# 기타
*.pyc
.pytest_cache/
```

#### Git 명령어 실행

```bash
# 현재 상태 확인
git status

# 모든 파일 추가 (첫 번째 커밋)
git add .

# 커밋 메시지와 함께 커밋
git commit -m "Initial commit: Hotel Management System with MySQL"

# GitHub 저장소를 원격 저장소로 추가
# YOUR_USERNAME과 YOUR_REPO_NAME을 실제 값으로 변경
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 또는 SSH를 사용하는 경우:
# git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git

# GitHub에 Push
git branch -M main
git push -u origin main
```

**주의**: 
- GitHub 사용자 이름과 저장소 이름을 정확히 입력하세요
- 첫 번째 push 시 GitHub 로그인 정보를 입력해야 할 수 있습니다

### 1.3 인증 문제 해결

#### Personal Access Token 사용 (권장)

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. **"Generate new token"** 클릭
3. 권한 선택:
   - `repo` (전체 체크)
4. **"Generate token"** 클릭
5. 생성된 토큰을 복사 (다시 볼 수 없으므로 저장!)
6. Push 시 비밀번호 대신 이 토큰 사용

```bash
# Push 시도
git push -u origin main

# Username: GitHub 사용자 이름
# Password: Personal Access Token (비밀번호 아님!)
```

---

## 2단계: GCP 서버에서 코드 Clone

### 2.1 GCP 서버 접속

```bash
# SSH로 GCP 서버 접속
# YOUR_INSTANCE_IP를 실제 IP로 변경
ssh -i ~/.ssh/YOUR_KEY_FILE.pem USERNAME@YOUR_INSTANCE_IP

# 또는 gcloud 명령어 사용
gcloud compute ssh INSTANCE_NAME --zone=ZONE_NAME
```

### 2.2 필요한 도구 설치 확인

```bash
# Git 설치 확인
git --version

# Git이 없으면 설치 (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install git -y

# Python 설치 확인
python3 --version

# MySQL 클라이언트 설치 확인
mysql --version
```

### 2.3 코드 Clone

```bash
# 프로젝트를 저장할 디렉토리로 이동 (예: 홈 디렉토리)
cd ~

# GitHub에서 코드 Clone
# YOUR_USERNAME과 YOUR_REPO_NAME을 실제 값으로 변경
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 또는 SSH를 사용하는 경우:
# git clone git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git

# 프로젝트 디렉토리로 이동
cd YOUR_REPO_NAME
```

### 2.3.1 Private 저장소인 경우

Private 저장소를 clone하려면 인증이 필요합니다:

```bash
# Personal Access Token 사용
git clone https://YOUR_TOKEN@github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 또는 SSH 키 설정 (권장)
# 1. 서버에서 SSH 키 생성
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. 공개 키 복사
cat ~/.ssh/id_ed25519.pub

# 3. GitHub → Settings → SSH and GPG keys → New SSH key
# 4. 복사한 공개 키 붙여넣기

# 5. SSH로 Clone
git clone git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
```

---

## 3단계: 서버에서 환경 설정

### 3.1 .env 파일 생성

```bash
# backend 디렉토리로 이동
cd ~/YOUR_REPO_NAME/backend

# .env 파일 생성
nano .env
# 또는
vim .env
```

`.env` 파일 내용 (서버의 MySQL 설정에 맞게 수정):

```env
# MySQL 설정 (GCP 서버의 MySQL)
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=서버의_MySQL_비밀번호
MYSQL_DATABASE=hotel_management

# CORS 설정 (프론트엔드 도메인)
CORS_ORIGINS=http://localhost:5173,https://your-domain.com
```

저장: `Ctrl + X`, `Y`, `Enter` (nano) 또는 `:wq` (vim)

### 3.2 필요한 패키지 설치

#### 백엔드

```bash
cd ~/YOUR_REPO_NAME/backend

# Python 가상환경 생성 (권장)
python3 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

#### 프론트엔드

```bash
cd ~/YOUR_REPO_NAME/frontend

# Node.js 설치 확인
node --version
npm --version

# Node.js가 없으면 설치
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 패키지 설치
npm install
```

### 3.3 MySQL 데이터베이스 설정

```bash
# MySQL 접속
mysql -u root -p

# 데이터베이스 생성
CREATE DATABASE hotel_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 사용자 생성 및 권한 부여 (선택사항)
CREATE USER 'hotel_user'@'localhost' IDENTIFIED BY '비밀번호';
GRANT ALL PRIVILEGES ON hotel_management.* TO 'hotel_user'@'localhost';
FLUSH PRIVILEGES;

# 종료
EXIT;
```

### 3.4 데이터베이스 테이블 생성

```bash
cd ~/YOUR_REPO_NAME/backend

# 가상환경 활성화 (이미 활성화되어 있으면 생략)
source venv/bin/activate

# 테이블 생성
python init_db.py
```

---

## 4단계: 서버에서 애플리케이션 실행

### 4.1 백엔드 실행

#### 개발 모드

```bash
cd ~/YOUR_REPO_NAME/backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 프로덕션 모드 (systemd 서비스 사용 권장)

`/etc/systemd/system/hotel-api.service` 파일 생성:

```ini
[Unit]
Description=Hotel Management API
After=network.target

[Service]
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/YOUR_REPO_NAME/backend
Environment="PATH=/home/YOUR_USERNAME/YOUR_REPO_NAME/backend/venv/bin"
ExecStart=/home/YOUR_USERNAME/YOUR_REPO_NAME/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

서비스 시작:

```bash
sudo systemctl daemon-reload
sudo systemctl enable hotel-api
sudo systemctl start hotel-api
sudo systemctl status hotel-api
```

### 4.2 프론트엔드 빌드 및 실행

#### 개발 모드

```bash
cd ~/YOUR_REPO_NAME/frontend
npm run dev -- --host 0.0.0.0
```

#### 프로덕션 빌드

```bash
cd ~/YOUR_REPO_NAME/frontend
npm run build

# Nginx로 서빙 (권장)
# 또는 Node.js로 서빙
npm install -g serve
serve -s dist -l 3000
```

---

## 5단계: 코드 업데이트 (향후)

### 로컬에서 변경사항 Push

```bash
# 로컬에서
cd F:\myproject\elimwood
git add .
git commit -m "변경사항 설명"
git push origin main
```

### 서버에서 Pull

```bash
# 서버에서
cd ~/YOUR_REPO_NAME
git pull origin main

# 백엔드 재시작 (systemd 사용 시)
sudo systemctl restart hotel-api

# 또는 수동 재시작
cd backend
source venv/bin/activate
# 기존 프로세스 종료 후
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 보안 주의사항

### 1. .env 파일은 절대 Git에 커밋하지 않기

`.gitignore`에 `.env`가 포함되어 있는지 확인:

```bash
# .gitignore 확인
cat .gitignore | grep .env
```

### 2. credentials.json도 커밋하지 않기

Google Sheets 인증 파일도 `.gitignore`에 포함되어 있는지 확인

### 3. 서버의 .env 파일 보안

```bash
# .env 파일 권한 설정
chmod 600 ~/YOUR_REPO_NAME/backend/.env
```

---

## 문제 해결

### Git Push 실패 시

```bash
# 원격 저장소 확인
git remote -v

# 원격 저장소 재설정
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 강제 Push (주의: 다른 사람과 협업 시 사용 금지)
git push -f origin main
```

### Clone 실패 시

```bash
# 네트워크 연결 확인
ping github.com

# Git 설정 확인
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 서버에서 MySQL 연결 실패 시

```bash
# MySQL 서비스 상태 확인
sudo systemctl status mysql

# MySQL 재시작
sudo systemctl restart mysql

# 방화벽 확인
sudo ufw status
```

---

## 체크리스트

- [ ] GitHub 저장소 생성
- [ ] 로컬에서 Git 초기화 및 첫 커밋
- [ ] .gitignore 파일 생성 및 확인
- [ ] GitHub에 Push 성공
- [ ] GCP 서버 접속
- [ ] 서버에서 Git 설치 확인
- [ ] 서버에서 코드 Clone
- [ ] 서버에 .env 파일 생성
- [ ] 서버에 MySQL 설치 및 데이터베이스 생성
- [ ] 서버에서 패키지 설치
- [ ] 서버에서 테이블 생성
- [ ] 서버에서 애플리케이션 실행
- [ ] 방화벽 설정 (필요 시)


