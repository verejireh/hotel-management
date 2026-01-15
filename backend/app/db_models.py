"""
SQLAlchemy 데이터베이스 모델 정의
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Customer(Base):
    """고객 테이블"""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    nationality = Column(String(100), nullable=True)
    
    # 관계
    reservations = relationship("Reservation", back_populates="customer")


class BookingPlatform(Base):
    """예약 플랫폼 테이블"""
    __tablename__ = "booking_platforms"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), nullable=False)  # Airbnb, Agoda, Hotels.com 등
    api_key = Column(String(255), nullable=True)
    webhook_url = Column(String(500), nullable=True)
    
    # 관계
    reservations = relationship("Reservation", back_populates="platform")


class Room(Base):
    """객실 테이블"""
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    room_number = Column(String(50), nullable=False, unique=True)
    room_type = Column(String(100), nullable=False)  # Standard, Deluxe, Suite 등
    max_guests = Column(Integer, nullable=False)
    price_per_night = Column(Float, nullable=False)
    status = Column(String(50), default="available")  # available, occupied, maintenance, cleaning
    
    # 관계
    reservations = relationship("Reservation", back_populates="room")


class Reservation(Base):
    """예약 테이블"""
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    platform_id = Column(Integer, ForeignKey("booking_platforms.id"), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    guests = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(50), default="Reserved")  # Reserved, Checked in, Checked out
    booking_reference = Column(String(255), nullable=False)  # 외부 플랫폼 예약 번호
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # 관계
    customer = relationship("Customer", back_populates="reservations")
    room = relationship("Room", back_populates="reservations")
    platform = relationship("BookingPlatform", back_populates="reservations")
    room_notes = relationship("RoomNote", back_populates="reservation")


class Admin(Base):
    """관리자 테이블"""
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    role = Column(String(100), nullable=True)  # manager, staff 등
    is_active = Column(Boolean, default=True)
    
    # 관계
    room_notes = relationship("RoomNote", back_populates="admin")


class RoomNote(Base):
    """객실 노트 테이블"""
    __tablename__ = "room_notes"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    room_id = Column(String(50), nullable=False)  # room_number를 문자열로 저장
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    note_type = Column(String(50), nullable=False)  # urgent, after_checkout
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), default="pending")  # pending, completed
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=True)
    progress = Column(String(50), nullable=True)  # confirm, In progress, finished
    
    # 관계
    admin = relationship("Admin", back_populates="room_notes")
    reservation = relationship("Reservation", back_populates="room_notes")


