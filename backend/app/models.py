from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class Customer(BaseModel):
    id: Optional[str] = None
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    nationality: Optional[str] = None


class BookingPlatform(BaseModel):
    id: Optional[str] = None
    name: str  # Airbnb, Agoda, Hotels.com, Rakuten 등
    api_key: Optional[str] = None
    webhook_url: Optional[str] = None


class Room(BaseModel):
    id: Optional[str] = None
    room_number: str
    room_type: str  # Standard, Deluxe, Suite 등
    max_guests: int
    price_per_night: float
    status: str = "available"  # available, occupied, maintenance, cleaning


class Reservation(BaseModel):
    id: Optional[str] = None
    customer_id: str
    room_id: str
    platform_id: str
    check_in: date
    check_out: date
    guests: int
    total_price: float
    status: str = "Reserved"  # Reserved, Checked in, Checked out
    booking_reference: str  # 외부 플랫폼 예약 번호
    notes: Optional[str] = None
    created_at: Optional[datetime] = None


class ReservationCreate(BaseModel):
    customer_id: str
    room_id: str
    platform_id: str
    check_in: date
    check_out: date
    guests: int
    total_price: float
    booking_reference: str
    notes: Optional[str] = None
    status: Optional[str] = "Reserved"  # 기본값: Reserved


class CheckInOutSummary(BaseModel):
    check_ins: list[Reservation]
    check_outs: list[Reservation]
    date: date


class Admin(BaseModel):
    id: Optional[str] = None
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None  # manager, staff, etc.
    is_active: bool = True


class RoomNote(BaseModel):
    id: Optional[str] = None
    room_id: str
    admin_id: str
    note_type: str  # urgent, after_checkout
    title: str
    description: str
    status: str = "pending"  # pending, completed
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    reservation_id: Optional[str] = None  # 체크아웃 후 작업인 경우 연결된 예약 ID
    progress: Optional[str] = None  # confirm, In progress, finished


class RoomNoteCreate(BaseModel):
    room_id: str
    admin_id: str
    note_type: str
    title: str
    description: str
    reservation_id: Optional[str] = None
    progress: Optional[str] = None  # confirm, In progress, finished

