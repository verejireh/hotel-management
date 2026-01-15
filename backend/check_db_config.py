"""
데이터베이스 설정 확인 스크립트
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 50)
print("현재 MySQL 설정 확인")
print("=" * 50)
print()

mysql_host = os.getenv("MYSQL_HOST", "localhost")
mysql_port = os.getenv("MYSQL_PORT", "3306")
mysql_user = os.getenv("MYSQL_USER", "root")
mysql_password = os.getenv("MYSQL_PASSWORD", "")
mysql_database = os.getenv("MYSQL_DATABASE", "hotel_management")

print(f"MYSQL_HOST: {mysql_host}")
print(f"MYSQL_PORT: {mysql_port}")
print(f"MYSQL_USER: {mysql_user}")
print(f"MYSQL_PASSWORD: {'*' * len(mysql_password) if mysql_password else '(비어있음)'}")
print(f"MYSQL_DATABASE: {mysql_database}")
print()

if mysql_host != "localhost" and mysql_host != "127.0.0.1":
    print("[WARNING] 원격 MySQL 서버를 사용하고 있습니다!")
    print(f"   현재 호스트: {mysql_host}")
    print()
    print("로컬 MySQL을 사용하려면:")
    print("  1. backend/.env 파일을 생성하거나 편집하세요")
    print("  2. MYSQL_HOST=localhost 로 설정하세요")
else:
    print("[OK] 로컬 MySQL 설정이 감지되었습니다.")
    print()

print("=" * 50)

