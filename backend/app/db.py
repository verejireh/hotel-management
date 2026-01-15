"""
MySQL 데이터베이스 클래스 (GoogleSheetsDB와 동일한 인터페이스)
"""
from typing import List, Dict, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.database import SessionLocal
from app.db_models import (
    Customer, Room, Reservation, Admin, RoomNote, BookingPlatform
)
from app.models import (
    Customer as CustomerModel,
    Room as RoomModel,
    Reservation as ReservationModel,
    Admin as AdminModel,
    RoomNote as RoomNoteModel
)


class MySQLDB:
    """MySQL 데이터베이스 클래스 (GoogleSheetsDB와 호환되는 인터페이스)"""
    
    def __init__(self):
        self.db: Session = SessionLocal()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
    
    def _to_dict(self, obj, model_class=None):
        """SQLAlchemy 객체를 딕셔너리로 변환"""
        if obj is None:
            return None
        
        result = {}
        for column in obj.__table__.columns:
            value = getattr(obj, column.name)
            # datetime을 문자열로 변환
            if isinstance(value, datetime):
                value = value.isoformat()
            elif isinstance(value, date):
                value = value.isoformat()
            result[column.name] = value
        
        # ID를 문자열로 변환 (Google Sheets와 호환)
        if 'id' in result:
            result['id'] = str(result['id'])
        
        return result
    
    # Customers 관련 메서드
    def get_customers(self) -> List[Dict]:
        """모든 고객 조회"""
        customers = self.db.query(Customer).all()
        return [self._to_dict(c) for c in customers]
    
    def get_customer(self, customer_id: str) -> Optional[Dict]:
        """고객 조회"""
        customer = self.db.query(Customer).filter(Customer.id == int(customer_id)).first()
        return self._to_dict(customer) if customer else None
    
    def create_customer(self, customer: Dict) -> Dict:
        """고객 생성"""
        new_customer = Customer(
            name=customer.get('name'),
            email=customer.get('email'),
            phone=customer.get('phone'),
            nationality=customer.get('nationality')
        )
        self.db.add(new_customer)
        self.db.commit()
        self.db.refresh(new_customer)
        return self._to_dict(new_customer)
    
    # Rooms 관련 메서드
    def get_rooms(self) -> List[Dict]:
        """모든 객실 조회"""
        rooms = self.db.query(Room).all()
        return [self._to_dict(r) for r in rooms]
    
    def get_room(self, room_id: str) -> Optional[Dict]:
        """객실 조회 (room_id는 room_number 또는 id)"""
        # 먼저 room_number로 시도
        room = self.db.query(Room).filter(Room.room_number == room_id).first()
        if not room:
            # id로 시도
            try:
                room = self.db.query(Room).filter(Room.id == int(room_id)).first()
            except ValueError:
                pass
        return self._to_dict(room) if room else None
    
    def update_room_status(self, room_id: str, status: str):
        """객실 상태 업데이트"""
        room = self.db.query(Room).filter(Room.room_number == room_id).first()
        if not room:
            try:
                room = self.db.query(Room).filter(Room.id == int(room_id)).first()
            except ValueError:
                pass
        
        if not room:
            raise ValueError(f"Room with id {room_id} not found")
        
        room.status = status
        self.db.commit()
    
    def create_room(self, room: Dict) -> Dict:
        """객실 생성"""
        new_room = Room(
            room_number=room.get('room_number'),
            room_type=room.get('room_type'),
            max_guests=int(room.get('max_guests', 0)),
            price_per_night=float(room.get('price_per_night', 0)),
            status=room.get('status', 'available')
        )
        self.db.add(new_room)
        self.db.commit()
        self.db.refresh(new_room)
        return self._to_dict(new_room)
    
    # Booking Platforms 관련 메서드
    def get_platforms(self) -> List[Dict]:
        """모든 예약 플랫폼 조회"""
        platforms = self.db.query(BookingPlatform).all()
        return [self._to_dict(p) for p in platforms]
    
    def create_platform(self, platform: Dict) -> Dict:
        """예약 플랫폼 생성"""
        new_platform = BookingPlatform(
            name=platform.get('name'),
            api_key=platform.get('api_key'),
            webhook_url=platform.get('webhook_url')
        )
        self.db.add(new_platform)
        self.db.commit()
        self.db.refresh(new_platform)
        return self._to_dict(new_platform)
    
    # Reservations 관련 메서드
    def get_reservations(self) -> List[Dict]:
        """모든 예약 조회"""
        reservations = self.db.query(Reservation).all()
        result = []
        for r in reservations:
            res_dict = self._to_dict(r)
            # customer_id, room_id, platform_id를 문자열로 변환
            if res_dict:
                res_dict['customer_id'] = str(res_dict.get('customer_id', ''))
                res_dict['room_id'] = str(res_dict.get('room_id', ''))
                res_dict['platform_id'] = str(res_dict.get('platform_id', ''))
            result.append(res_dict)
        return result
    
    def get_reservation(self, reservation_id: str) -> Optional[Dict]:
        """예약 조회"""
        reservation = self.db.query(Reservation).filter(
            Reservation.id == int(reservation_id)
        ).first()
        if reservation:
            res_dict = self._to_dict(reservation)
            res_dict['customer_id'] = str(res_dict.get('customer_id', ''))
            res_dict['room_id'] = str(res_dict.get('room_id', ''))
            res_dict['platform_id'] = str(res_dict.get('platform_id', ''))
            return res_dict
        return None
    
    def create_reservation(self, reservation: Dict) -> Dict:
        """예약 생성"""
        new_reservation = Reservation(
            customer_id=int(reservation.get('customer_id')),
            room_id=int(reservation.get('room_id')),
            platform_id=int(reservation.get('platform_id')),
            check_in=reservation.get('check_in'),
            check_out=reservation.get('check_out'),
            guests=int(reservation.get('guests')),
            total_price=float(reservation.get('total_price')),
            status=reservation.get('status', 'Reserved'),
            booking_reference=reservation.get('booking_reference'),
            notes=reservation.get('notes')
        )
        self.db.add(new_reservation)
        self.db.commit()
        self.db.refresh(new_reservation)
        res_dict = self._to_dict(new_reservation)
        res_dict['customer_id'] = str(res_dict.get('customer_id', ''))
        res_dict['room_id'] = str(res_dict.get('room_id', ''))
        res_dict['platform_id'] = str(res_dict.get('platform_id', ''))
        return res_dict
    
    def update_reservation_status(self, reservation_id: str, status: str):
        """예약 상태 업데이트"""
        valid_statuses = ['Reserved', 'Checked in', 'Checked out']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        reservation = self.db.query(Reservation).filter(
            Reservation.id == int(reservation_id)
        ).first()
        
        if not reservation:
            raise ValueError(f"Reservation with id {reservation_id} not found")
        
        reservation.status = status
        self.db.commit()
        
        # 객실 상태도 업데이트
        if status == 'Checked in':
            reservation.room.status = 'occupied'
        elif status == 'Checked out':
            reservation.room.status = 'cleaning'
        self.db.commit()
    
    def check_duplicate_reservation(self, room_id: str, check_in: str, check_out: str, exclude_id: str = None) -> bool:
        """중복 예약 체크"""
        check_in_date = check_in if isinstance(check_in, date) else datetime.strptime(str(check_in), '%Y-%m-%d').date()
        check_out_date = check_out if isinstance(check_out, date) else datetime.strptime(str(check_out), '%Y-%m-%d').date()
        
        query = self.db.query(Reservation).filter(
            Reservation.room_id == int(room_id),
            Reservation.status != 'cancelled'
        )
        
        if exclude_id:
            query = query.filter(Reservation.id != int(exclude_id))
        
        # 날짜 겹침 체크
        overlapping = query.filter(
            and_(
                Reservation.check_in <= check_out_date,
                Reservation.check_out >= check_in_date
            )
        ).first()
        
        return overlapping is not None
    
    # Admins 관련 메서드
    def get_admins(self) -> List[Dict]:
        """모든 관리자 조회"""
        admins = self.db.query(Admin).all()
        return [self._to_dict(a) for a in admins]
    
    def get_admin(self, admin_id: str) -> Optional[Dict]:
        """관리자 조회"""
        admin = self.db.query(Admin).filter(Admin.id == int(admin_id)).first()
        return self._to_dict(admin) if admin else None
    
    def create_admin(self, admin: Dict) -> Dict:
        """관리자 생성"""
        new_admin = Admin(
            name=admin.get('name'),
            email=admin.get('email'),
            phone=admin.get('phone'),
            role=admin.get('role'),
            is_active=admin.get('is_active', True)
        )
        self.db.add(new_admin)
        self.db.commit()
        self.db.refresh(new_admin)
        return self._to_dict(new_admin)
    
    def delete_admin(self, admin_id: str):
        """관리자 삭제"""
        admin = self.db.query(Admin).filter(Admin.id == int(admin_id)).first()
        if not admin:
            raise ValueError(f"Admin with id {admin_id} not found")
        
        self.db.delete(admin)
        self.db.commit()
    
    # Notes 관련 메서드
    def get_notes(self) -> List[Dict]:
        """모든 노트 조회"""
        notes = self.db.query(RoomNote).all()
        result = []
        for note in notes:
            note_dict = self._to_dict(note)
            if note_dict:
                # admin_id를 문자열로 변환
                note_dict['admin_id'] = str(note_dict.get('admin_id', ''))
                # reservation_id를 문자열로 변환 (None일 수 있음)
                if note_dict.get('reservation_id'):
                    note_dict['reservation_id'] = str(note_dict['reservation_id'])
                else:
                    note_dict['reservation_id'] = ''
            result.append(note_dict)
        return result
    
    def get_note(self, note_id: str) -> Optional[Dict]:
        """노트 조회"""
        note = self.db.query(RoomNote).filter(RoomNote.id == int(note_id)).first()
        if note:
            note_dict = self._to_dict(note)
            note_dict['admin_id'] = str(note_dict.get('admin_id', ''))
            if note_dict.get('reservation_id'):
                note_dict['reservation_id'] = str(note_dict['reservation_id'])
            else:
                note_dict['reservation_id'] = ''
            return note_dict
        return None
    
    def get_notes_by_room(self, room_id: str) -> List[Dict]:
        """객실별 노트 조회"""
        notes = self.db.query(RoomNote).filter(RoomNote.room_id == room_id).all()
        result = []
        for note in notes:
            note_dict = self._to_dict(note)
            if note_dict:
                note_dict['admin_id'] = str(note_dict.get('admin_id', ''))
                if note_dict.get('reservation_id'):
                    note_dict['reservation_id'] = str(note_dict['reservation_id'])
                else:
                    note_dict['reservation_id'] = ''
            result.append(note_dict)
        return result
    
    def create_note(self, note: Dict) -> Dict:
        """노트 생성"""
        # admin_id를 이름에서 ID로 변환 (필요시)
        admin_id = note.get('admin_id')
        if isinstance(admin_id, str) and not admin_id.isdigit():
            # 이름으로 관리자 찾기
            admin = self.db.query(Admin).filter(Admin.name == admin_id).first()
            if admin:
                admin_id = admin.id
            else:
                raise ValueError(f"Admin with name {admin_id} not found")
        
        # room_id를 room_number로 변환 (필요시)
        room_id = note.get('room_id')
        if isinstance(room_id, str) and room_id.isdigit():
            # ID로 객실 찾기
            room = self.db.query(Room).filter(Room.id == int(room_id)).first()
            if room:
                room_id = room.room_number
        
        new_note = RoomNote(
            room_id=str(room_id),
            admin_id=int(admin_id),
            note_type=note.get('note_type'),
            title=note.get('title'),
            description=note.get('description'),
            reservation_id=int(note.get('reservation_id')) if note.get('reservation_id') else None,
            progress=note.get('progress')
        )
        self.db.add(new_note)
        self.db.commit()
        self.db.refresh(new_note)
        note_dict = self._to_dict(new_note)
        note_dict['admin_id'] = str(note_dict.get('admin_id', ''))
        if note_dict.get('reservation_id'):
            note_dict['reservation_id'] = str(note_dict['reservation_id'])
        else:
            note_dict['reservation_id'] = ''
        return note_dict
    
    def update_note_progress(self, note_id: str, progress: str):
        """노트 진행 상태 업데이트"""
        note = self.db.query(RoomNote).filter(RoomNote.id == int(note_id)).first()
        if not note:
            raise ValueError(f"Note with id {note_id} not found")
        
        note.progress = progress
        if progress == 'finished':
            note.status = 'completed'
            note.completed_at = datetime.now()
        self.db.commit()
    
    def get_notes_by_progress(self, progress: str = None) -> List[Dict]:
        """진행 상태별 노트 조회"""
        query = self.db.query(RoomNote)
        
        if progress is None:
            # progress가 None이면 모든 노트 반환
            notes = query.all()
        elif progress == '':
            # progress가 빈 문자열이면 progress가 None인 노트만
            notes = query.filter(RoomNote.progress.is_(None)).all()
        else:
            # 특정 progress 값으로 필터링
            notes = query.filter(RoomNote.progress == progress).all()
        
        result = []
        for note in notes:
            note_dict = self._to_dict(note)
            if note_dict:
                note_dict['admin_id'] = str(note_dict.get('admin_id', ''))
                if note_dict.get('reservation_id'):
                    note_dict['reservation_id'] = str(note_dict['reservation_id'])
                else:
                    note_dict['reservation_id'] = ''
            result.append(note_dict)
        return result
    
    def get_urgent_notes(self) -> List[Dict]:
        """긴급 노트 조회"""
        notes = self.db.query(RoomNote).filter(
            RoomNote.note_type == 'urgent',
            RoomNote.status == 'pending'
        ).all()
        result = []
        for note in notes:
            note_dict = self._to_dict(note)
            if note_dict:
                note_dict['admin_id'] = str(note_dict.get('admin_id', ''))
                if note_dict.get('reservation_id'):
                    note_dict['reservation_id'] = str(note_dict['reservation_id'])
                else:
                    note_dict['reservation_id'] = ''
            result.append(note_dict)
        return result
    
    def get_after_checkout_notes(self) -> List[Dict]:
        """체크아웃 후 노트 조회"""
        notes = self.db.query(RoomNote).filter(
            RoomNote.note_type == 'after_checkout',
            RoomNote.status == 'pending'
        ).all()
        result = []
        for note in notes:
            note_dict = self._to_dict(note)
            if note_dict:
                note_dict['admin_id'] = str(note_dict.get('admin_id', ''))
                if note_dict.get('reservation_id'):
                    note_dict['reservation_id'] = str(note_dict['reservation_id'])
                else:
                    note_dict['reservation_id'] = ''
            result.append(note_dict)
        return result

