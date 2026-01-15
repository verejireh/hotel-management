"""
데이터베이스 초기화 스크립트
MySQL 데이터베이스와 테이블을 생성합니다.
"""
from app.database import engine, Base
from app.db_models import (
    Customer, Room, Reservation, Admin, RoomNote, BookingPlatform
)

def init_db():
    """데이터베이스 테이블 생성"""
    print("Creating database tables...")
    print("This will create the following tables:")
    print("  - customers")
    print("  - rooms")
    print("  - booking_platforms")
    print("  - reservations")
    print("  - admins")
    print("  - room_notes")
    print()
    
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()

