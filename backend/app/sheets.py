import os
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pydantic_settings import BaseSettings
import json


class Settings(BaseSettings):
    google_sheets_credentials_file: str = "credentials.json"
    google_sheets_spreadsheet_id: str = "1-z7qb1HZOWaqEYZJ1iwxmt1zzD1NTSX7CSk3RDFkM0Q"
    
    class Config:
        env_file = ".env"


settings = Settings()


class GoogleSheetsDB:
    def __init__(self):
        self.service = None
        self.spreadsheet_id = settings.google_sheets_spreadsheet_id
        
        # 시트 ID 검증
        if not self.spreadsheet_id:
            raise ValueError(
                "Google Sheets Spreadsheet ID is not set. "
                "Please set GOOGLE_SHEETS_SPREADSHEET_ID in .env file or in sheets.py"
            )
        
        self._initialize_service()
    
    def _initialize_service(self):
        """Google Sheets API 서비스 초기화"""
        try:
            if os.path.exists(settings.google_sheets_credentials_file):
                creds = service_account.Credentials.from_service_account_file(
                    settings.google_sheets_credentials_file,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
            else:
                # 개발용: 환경변수에서 직접 읽기
                creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS_JSON')
                if creds_json:
                    creds_info = json.loads(creds_json)
                    creds = service_account.Credentials.from_service_account_info(
                        creds_info,
                        scopes=['https://www.googleapis.com/auth/spreadsheets']
                    )
                else:
                    raise FileNotFoundError("Google Sheets credentials not found")
            
            self.service = build('sheets', 'v4', credentials=creds)
        except Exception as e:
            print(f"Error initializing Google Sheets service: {e}")
            raise
    
    def _read_sheet(self, sheet_name: str, range_name: str = None) -> List[List]:
        """시트에서 데이터 읽기"""
        try:
            if range_name is None:
                # 각 시트별 최대 열 수 정의 (실제 사용하는 열 수에 맞춤)
                max_cols = {
                    "customers": "E",  # 5개 열
                    "reservation": "L",  # 12개 열
                    "booking_platforms": "D",  # 4개 열
                    "rooms": "F",  # 6개 열
                    "admin": "D",  # 4개 열
                    "note": "F",  # A~F열 (Room Number, Name, Note Type, Title, Description, Progress 등)
                }
                # 기본값은 충분히 큰 범위 (M열까지, 13개 열)
                col_range = max_cols.get(sheet_name, "M")
                range_name = f"{sheet_name}!A:{col_range}"
            else:
                range_name = f"{sheet_name}!{range_name}"
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            return result.get('values', [])
        except HttpError as error:
            print(f"Error reading sheet {sheet_name}: {error}")
            return []
    
    def _write_sheet(self, sheet_name: str, values: List[List], range_name: str = None):
        """시트에 데이터 쓰기"""
        try:
            if range_name is None:
                range_name = f"{sheet_name}!A1"
            else:
                range_name = f"{sheet_name}!{range_name}"
            
            body = {'values': values}
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
        except HttpError as error:
            print(f"Error writing to sheet {sheet_name}: {error}")
            raise
    
    def _append_to_sheet(self, sheet_name: str, values: List[List]):
        """시트에 데이터 추가"""
        try:
            # 각 시트별 최대 열 수에 맞춰 쓰기
            max_cols = {
                "customers": "E",
                "reservation": "M",
                "booking_platforms": "D",
                "rooms": "F",
                "admin": "D",
                "note": "G",
            }
            col_range = max_cols.get(sheet_name, "M")
            range_name = f"{sheet_name}!A:{col_range}"
            body = {'values': values}
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
        except HttpError as error:
            print(f"Error appending to sheet {sheet_name}: {error}")
            raise
    
    def _get_next_id(self, sheet_name: str) -> str:
        """다음 ID 생성"""
        data = self._read_sheet(sheet_name)
        if len(data) <= 1:  # 헤더만 있거나 비어있음
            return "1"
        try:
            ids = [int(row[0]) for row in data[1:] if row and row[0].isdigit()]
            return str(max(ids) + 1) if ids else "1"
        except:
            return "1"
    
    # Customers 관련 메서드
    def get_customers(self) -> List[Dict]:
        """모든 고객 조회"""
        data = self._read_sheet("customers")
        if len(data) < 2:
            return []
        
        headers = data[0]
        customers = []
        for row in data[1:]:
            if row:
                customer = dict(zip(headers, row + [''] * (len(headers) - len(row))))
                customers.append(customer)
        return customers
    
    def get_customer(self, customer_id: str) -> Optional[Dict]:
        """고객 조회"""
        customers = self.get_customers()
        return next((c for c in customers if c.get('id') == customer_id), None)
    
    def create_customer(self, customer: Dict) -> Dict:
        """고객 생성"""
        customer['id'] = self._get_next_id("customers")
        headers = ["id", "name", "email", "phone", "nationality"]
        row = [customer.get(h, '') for h in headers]
        self._append_to_sheet("customers", [row])
        return customer
    
    # Rooms 관련 메서드
    def get_rooms(self) -> List[Dict]:
        """모든 방 조회"""
        data = self._read_sheet("rooms")
        if len(data) < 2:
            return []
        
        headers = data[0]
        rooms = []
        for row in data[1:]:
            if row:
                room = dict(zip(headers, row + [''] * (len(headers) - len(row))))
                rooms.append(room)
        return rooms
    
    def get_room(self, room_id: str) -> Optional[Dict]:
        """방 조회"""
        rooms = self.get_rooms()
        return next((r for r in rooms if r.get('id') == room_id), None)
    
    def update_room_status(self, room_id: str, status: str):
        """방 상태 업데이트"""
        data = self._read_sheet("rooms")
        if len(data) < 2:
            print("Rooms sheet is empty")
            return
        
        headers = data[0]
        header_map = {h.lower().replace('-', '_'): i for i, h in enumerate(headers)}
        
        # status 열 찾기
        status_col = header_map.get('status', None)
        if status_col is None:
            print("Status column not found in rooms sheet")
            return
        
        id_col = header_map.get('id', 0)
        
        try:
            for i, row in enumerate(data[1:], start=2):
                if row and len(row) > id_col and str(row[id_col]) == str(room_id):
                    if len(row) <= status_col:
                        row.extend([''] * (status_col - len(row) + 1))
                    row[status_col] = status
                    # range_name에는 시트 이름을 포함하지 않음 (_write_sheet에서 추가됨)
                    range_name = f"{chr(65 + status_col)}{i}"
                    self._write_sheet("rooms", [[status]], range_name)
                    print(f"Room {room_id} status updated to {status}")
                    return
            print(f"Room with id {room_id} not found")
        except Exception as e:
            print(f"Error updating room status: {e}")
            raise
    
    # Booking Platforms 관련 메서드
    def get_platforms(self) -> List[Dict]:
        """모든 예약 플랫폼 조회"""
        data = self._read_sheet("booking_platforms")
        if len(data) < 2:
            return []
        
        headers = data[0]
        platforms = []
        for row in data[1:]:
            if row:
                platform = dict(zip(headers, row + [''] * (len(headers) - len(row))))
                platforms.append(platform)
        return platforms
    
    # Reservations 관련 메서드
    def get_reservations(self) -> List[Dict]:
        """모든 예약 조회"""
        data = self._read_sheet("reservation")
        if len(data) < 2:
            return []
        
        headers = data[0]
        reservations = []
        for row in data[1:]:
            if row:
                reservation = dict(zip(headers, row + [''] * (len(headers) - len(row))))
                reservations.append(reservation)
        return reservations
    
    def get_reservation(self, reservation_id: str) -> Optional[Dict]:
        """예약 조회"""
        reservations = self.get_reservations()
        return next((r for r in reservations if r.get('id') == reservation_id), None)
    
    def create_reservation(self, reservation: Dict) -> Dict:
        """예약 생성"""
        reservation['id'] = self._get_next_id("reservation")
        # reservation 시트의 헤더 확인
        data = self._read_sheet("reservation")
        if len(data) == 0:
            raise ValueError("reservation sheet is empty or headers not found")
        
        headers = data[0]
        # 헤더를 소문자로 변환하여 인덱스 찾기
        header_map = {h.lower().replace('-', '_'): i for i, h in enumerate(headers)}
        
        # 새 행 생성 (헤더 순서에 맞춰)
        row = [''] * len(headers)
        
        # 데이터 매핑
        field_mapping = {
            'id': 'id',
            'customer_id': 'customer_id',
            'room_id': 'room_id',
            'platform_id': 'platform_id',
            'check_in': 'check_in',
            'check_out': 'check_out',
            'guests': 'guests',
            'total_price': 'total_price',
            'status': 'status',
            'booking_reference': 'booking_reference',
            'notes': 'notes',
            'created_at': 'created_at'
        }
        
        for field, key in field_mapping.items():
            if key in header_map:
                row[header_map[key]] = str(reservation.get(field, ''))
        
        self._append_to_sheet("reservation", [row])
        return reservation
    
    def update_reservation_status(self, reservation_id: str, status: str):
        """예약의 Status 업데이트"""
        valid_statuses = ['Reserved', 'Checked in', 'Checked out']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        data = self._read_sheet("reservation")
        if len(data) < 2:
            raise ValueError("Reservation sheet is empty")
        
        headers = data[0]
        header_map = {h.lower().replace('-', '_'): i for i, h in enumerate(headers)}
        
        # status 열 찾기
        status_col = header_map.get('status', None)
        if status_col is None:
            raise ValueError("Status column not found in reservation sheet")
        
        try:
            id_col = header_map.get('id', 0)
            
            for i, row in enumerate(data[1:], start=2):
                if row and len(row) > id_col and str(row[id_col]) == str(reservation_id):
                    if len(row) <= status_col:
                        row.extend([''] * (status_col - len(row) + 1))
                    row[status_col] = status
                    # range_name에는 시트 이름을 포함하지 않음 (_write_sheet에서 추가됨)
                    range_name = f"{chr(65 + status_col)}{i}"
                    self._write_sheet("reservation", [[status]], range_name)
                    return
            raise ValueError(f"Reservation with id {reservation_id} not found")
        except (ValueError, IndexError) as e:
            print(f"Error updating reservation status: {e}")
            raise
    
    def check_duplicate_reservation(self, room_id: str, check_in: str, check_out: str, exclude_id: str = None) -> bool:
        """중복 예약 체크"""
        reservations = self.get_reservations()
        check_in_date = check_in if isinstance(check_in, str) else str(check_in)
        check_out_date = check_out if isinstance(check_out, str) else str(check_out)
        
        for res in reservations:
            if exclude_id and res.get('id') == exclude_id:
                continue
            if res.get('room_id') != room_id:
                continue
            if res.get('status') in ['cancelled']:
                continue
            
            res_check_in = res.get('check_in', '')
            res_check_out = res.get('check_out', '')
            
            # 날짜 겹침 체크
            if (check_in_date <= res_check_out and check_out_date >= res_check_in):
                return True
        
        return False
    
    # Admins 관련 메서드
    def get_admins(self) -> List[Dict]:
        """모든 관리자 조회"""
        data = self._read_sheet("admin")
        if len(data) < 2:
            return []
        
        headers = data[0]
        # 컬럼명을 소문자로 변환하여 매핑 (대소문자 무시)
        header_map = {}
        for i, h in enumerate(headers):
            header_map[h.lower()] = i
        
        admins = []
        for row in data[1:]:
            if row:
                admin = {}
                # id는 자동 생성 (행 번호 사용)
                admin['id'] = str(len(admins) + 1)
                # 컬럼명 매핑
                if 'name' in header_map:
                    admin['name'] = row[header_map['name']] if len(row) > header_map['name'] else ''
                if 'email' in header_map:
                    admin['email'] = row[header_map['email']] if len(row) > header_map['email'] else ''
                if 'phone' in header_map:
                    admin['phone'] = row[header_map['phone']] if len(row) > header_map['phone'] else ''
                if 'role' in header_map:
                    admin['role'] = row[header_map['role']] if len(row) > header_map['role'] else ''
                admin['is_active'] = True  # 기본값
                admins.append(admin)
        return admins
    
    def get_admin(self, admin_id: str) -> Optional[Dict]:
        """관리자 조회"""
        admins = self.get_admins()
        return next((a for a in admins if a.get('id') == admin_id), None)
    
    def create_admin(self, admin: Dict) -> Dict:
        """관리자 생성"""
        # 시트의 헤더 확인
        data = self._read_sheet("admin")
        if len(data) == 0:
            raise ValueError("admin sheet is empty or headers not found")
        
        headers = data[0]
        # 헤더를 소문자로 변환하여 인덱스 찾기
        header_map = {h.lower(): i for i, h in enumerate(headers)}
        
        # 새 행 생성 (헤더 순서에 맞춰)
        row = [''] * len(headers)
        
        # 데이터 매핑
        if 'name' in header_map:
            row[header_map['name']] = str(admin.get('name', ''))
        if 'email' in header_map:
            row[header_map['email']] = str(admin.get('email', ''))
        if 'phone' in header_map:
            row[header_map['phone']] = str(admin.get('phone', ''))
        if 'role' in header_map:
            row[header_map['role']] = str(admin.get('role', ''))
        
        # id는 자동 생성 (행 번호)
        admin['id'] = str(len(data))
        self._append_to_sheet("admin", [row])
        return admin
    
    def delete_admin(self, admin_id: str):
        """관리자 삭제"""
        data = self._read_sheet("admin")
        if len(data) < 2:
            raise ValueError("Admin sheet is empty or has no data rows")
        
        headers = data[0]
        header_map = {h.lower(): i for i, h in enumerate(headers)}
        
        # admin_id는 get_admins에서 len(admins) + 1로 생성되므로
        # 실제 행 번호는 헤더(1행) 다음부터 시작하므로 admin_id를 인덱스로 사용
        # 첫 번째 admin: ID = "1", 실제 행 번호 = 2 (인덱스 1)
        # 두 번째 admin: ID = "2", 실제 행 번호 = 3 (인덱스 2)
        try:
            admin_index = int(admin_id) - 1  # ID를 인덱스로 변환 (0-based)
            if admin_index < 0 or admin_index >= len(data) - 1:
                raise ValueError(f"Admin with id {admin_id} not found")
            
            # 실제 행 번호는 헤더 다음부터 시작 (1-based)
            row_index = admin_index + 2  # 헤더(1) + 인덱스(0-based) + 1 = 2-based
            
        except ValueError:
            # ID가 숫자가 아니면 이름으로 찾기
            name_col = header_map.get('name', 0)
            row_index = None
            for i, row in enumerate(data[1:], start=2):
                if row and len(row) > name_col:
                    # admin_id가 이름과 일치하는지 확인
                    if str(row[name_col]).strip() == str(admin_id).strip():
                        row_index = i
                        break
            
            if row_index is None:
                raise ValueError(f"Admin with id {admin_id} not found")
        
        # Google Sheets API를 사용하여 행 삭제
        try:
            if not self.service:
                self._initialize_service()
            
            # batchUpdate를 사용하여 행 삭제
            requests = [{
                'deleteDimension': {
                    'range': {
                        'sheetId': self._get_sheet_id("admin"),
                        'dimension': 'ROWS',
                        'startIndex': row_index - 1,  # 0-based index
                        'endIndex': row_index
                    }
                }
            }]
            
            body = {
                'requests': requests
            }
            
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()
        except HttpError as error:
            print(f"Error deleting admin: {error}")
            raise ValueError(f"Failed to delete admin: {error}")
    
    def _get_sheet_id(self, sheet_name: str) -> int:
        """시트 이름으로 시트 ID 가져오기"""
        try:
            if not self.service:
                self._initialize_service()
            
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            for sheet in spreadsheet.get('sheets', []):
                if sheet['properties']['title'].lower() == sheet_name.lower():
                    return sheet['properties']['sheetId']
            
            raise ValueError(f"Sheet '{sheet_name}' not found")
        except HttpError as error:
            print(f"Error getting sheet ID: {error}")
            raise
    
    # Note 시트 관련 메서드 (room_notes 대신 note 시트 사용)
    def get_notes(self) -> List[Dict]:
        """모든 노트 조회"""
        try:
            import sys
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"[SHEETS] get_notes: Starting to read note sheet")
            data = self._read_sheet("note")
            logger.error(f"[SHEETS] get_notes: Read {len(data)} rows from note sheet")
            print(f"[SHEETS] get_notes: Read {len(data)} rows from note sheet", file=sys.stderr, flush=True)
            print(f"[SHEETS] get_notes: Read {len(data)} rows from note sheet", flush=True)
            if len(data) < 2:
                print("[SHEETS] get_notes: Not enough data (need at least header + 1 row)", file=sys.stderr, flush=True)
                print("[SHEETS] get_notes: Not enough data (need at least header + 1 row)", flush=True)
                return []
            
            headers = data[0]
            import sys
            print(f"[SHEETS] get_notes: Headers = {headers}", file=sys.stderr, flush=True)
            print(f"[SHEETS] get_notes: Headers = {headers}", flush=True)
            print(f"[SHEETS] get_notes: Number of headers = {len(headers)}", flush=True)
            
            # 데이터 행 확인
            print(f"[SHEETS] get_notes: Number of data rows = {len(data) - 1}", flush=True)
            if len(data) > 1:
                for idx, row in enumerate(data[1:min(6, len(data))], start=2):  # 처음 5개 행만 출력
                    print(f"[SHEETS] get_notes: Row {idx} = {row}", file=sys.stderr, flush=True)
                    print(f"[SHEETS] get_notes: Row {idx} = {row}", flush=True)
            else:
                print(f"[SHEETS] get_notes: No data rows found!", file=sys.stderr, flush=True)
                print(f"[SHEETS] get_notes: No data rows found!", flush=True)
        except Exception as e:
            import sys
            print(f"[SHEETS ERROR] get_notes: Error reading sheet: {e}", file=sys.stderr, flush=True)
            print(f"[SHEETS ERROR] get_notes: Error reading sheet: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return []
        
        # 헤더를 소문자로 변환하여 매핑 (다양한 형식 지원)
        header_map = {}
        for i, h in enumerate(headers):
            if h:
                h_lower = h.lower().strip()
                header_map[h_lower] = i
                header_map[h_lower.replace(' ', '_')] = i
                header_map[h_lower.replace(' ', '')] = i
                header_map[h_lower.replace('-', '_')] = i
                header_map[h_lower.replace('-', '')] = i
                header_map[h_lower.replace(' ', '_').replace('-', '_')] = i
        
        print(f"get_notes: Header map keys = {list(header_map.keys())[:10]}...")
        
        notes = []
        for i, row in enumerate(data[1:], start=2):
            # 빈 행 체크: row가 존재하고 최소한 하나의 셀에 값이 있으면 처리
            row_has_data = row and len(row) > 0 and any(
                cell is not None and str(cell).strip() != '' 
                for cell in row if cell is not None
            )
            
            if not row_has_data:
                print(f"get_notes: Skipping row {i} (empty or no data)")
                continue
            
            # 노트 객체 생성
            note = {}
            note['id'] = str(i - 1)  # 행 번호를 ID로 사용
            
            # Room Number 또는 room_id
            room_value = ''
            for key in ['room_number', 'room_id', 'room number', 'roomnumber']:
                if key in header_map:
                    col_idx = header_map[key]
                    if len(row) > col_idx:
                        room_value = str(row[col_idx]).strip()
                    break
            note['room_id'] = room_value
            
            # Name 또는 admin_id 또는 role
            admin_value = ''
            for key in ['name', 'admin_id', 'admin id', 'adminid', 'role']:
                if key in header_map:
                    col_idx = header_map[key]
                    if len(row) > col_idx:
                        admin_value = str(row[col_idx]).strip()
                    break
            note['admin_id'] = admin_value
            
            # Note Type
            note_type_value = ''
            for key in ['note_type', 'note type', 'notetype']:
                if key in header_map:
                    col_idx = header_map[key]
                    if len(row) > col_idx:
                        note_type_value = str(row[col_idx]).strip()
                    break
            note['note_type'] = note_type_value
            
            # Title
            if 'title' in header_map:
                col_idx = header_map['title']
                note['title'] = str(row[col_idx]).strip() if len(row) > col_idx else ''
            else:
                note['title'] = ''
            
            # Description
            if 'description' in header_map:
                col_idx = header_map['description']
                note['description'] = str(row[col_idx]).strip() if len(row) > col_idx else ''
            else:
                note['description'] = ''
            
            # Progress
            if 'progress' in header_map:
                col_idx = header_map['progress']
                note['progress'] = str(row[col_idx]).strip() if len(row) > col_idx else ''
            else:
                note['progress'] = ''
            
            # Reservation ID
            reservation_value = ''
            for key in ['reservation_id', 'reservation id', 'reservationid']:
                if key in header_map:
                    col_idx = header_map[key]
                    if len(row) > col_idx:
                        reservation_value = str(row[col_idx]).strip()
                    break
            note['reservation_id'] = reservation_value
            
            # Status
            if 'status' in header_map:
                col_idx = header_map['status']
                note['status'] = str(row[col_idx]).strip() if len(row) > col_idx else 'pending'
            else:
                note['status'] = 'pending'
            
            # Created At
            created_at_value = ''
            for key in ['created_at', 'created at', 'createdat']:
                if key in header_map:
                    col_idx = header_map[key]
                    if len(row) > col_idx:
                        created_at_value = str(row[col_idx]).strip()
                    break
            note['created_at'] = created_at_value
            
            # Completed At
            completed_at_value = ''
            for key in ['completed_at', 'completed at', 'completedat']:
                if key in header_map:
                    col_idx = header_map[key]
                    if len(row) > col_idx:
                        completed_at_value = str(row[col_idx]).strip()
                    break
            note['completed_at'] = completed_at_value
            
            # 최소한 title이나 description이 있어야 노트로 인정
            if note.get('title') or note.get('description'):
                notes.append(note)
                import sys
                print(f"[SHEETS] get_notes: Added note {note.get('id')}: title='{note.get('title')}', room='{note.get('room_id')}'", flush=True)
                print(f"[SHEETS] get_notes: Added note {note.get('id')}: title='{note.get('title')}', room='{note.get('room_id')}'", file=sys.stderr, flush=True)
            else:
                import sys
                print(f"[SHEETS] get_notes: Skipped row {i} (no title or description): title='{note.get('title')}', desc='{note.get('description')}'", flush=True)
                print(f"[SHEETS] get_notes: Skipped row {i} (no title or description): title='{note.get('title')}', desc='{note.get('description')}'", file=sys.stderr, flush=True)
        
        import sys
        print(f"[SHEETS] get_notes: Returning {len(notes)} notes", flush=True)
        print(f"[SHEETS] get_notes: Returning {len(notes)} notes", file=sys.stderr, flush=True)
        
        # 디버깅: 실제로 읽은 데이터 확인
        if len(data) >= 2 and len(notes) == 0:
            print(f"[SHEETS DEBUG] Data has {len(data)} rows but notes is empty", file=sys.stderr, flush=True)
            print(f"[SHEETS DEBUG] Headers: {headers}", file=sys.stderr, flush=True)
            if len(data) > 1:
                print(f"[SHEETS DEBUG] First data row: {data[1]}", file=sys.stderr, flush=True)
        
        return notes
    
    def get_note(self, note_id: str) -> Optional[Dict]:
        """노트 조회"""
        notes = self.get_notes()
        return next((n for n in notes if n.get('id') == note_id), None)
    
    def get_notes_by_room(self, room_id: str) -> List[Dict]:
        """특정 방의 노트 조회"""
        notes = self.get_notes()
        return [n for n in notes if n.get('room_id') == room_id]
    
    def create_note(self, note: Dict) -> Dict:
        """노트 생성"""
        # note 시트의 헤더 확인
        data = self._read_sheet("note")
        if len(data) == 0:
            raise ValueError("note sheet is empty or headers not found")
        
        headers = data[0]
        # 헤더를 소문자로 변환하여 인덱스 찾기 (다양한 형식 지원)
        header_map = {}
        for i, h in enumerate(headers):
            if h:
                # 원본, 소문자, 공백/하이픈 제거 버전 모두 저장
                h_lower = h.lower().strip()
                header_map[h_lower] = i
                header_map[h_lower.replace(' ', '_')] = i
                header_map[h_lower.replace(' ', '')] = i
                header_map[h_lower.replace('-', '_')] = i
                header_map[h_lower.replace('-', '')] = i
                header_map[h_lower.replace(' ', '_').replace('-', '_')] = i
        
        # 새 행 생성 (헤더 순서에 맞춰)
        row = [''] * len(headers)
        
        # admin_id를 admin 이름으로 변환
        admin_id = note.get('admin_id', '')
        admin_name = ''
        if admin_id:
            try:
                admin_data = self.get_admin(admin_id)
                if admin_data:
                    admin_name = admin_data.get('name', '')
            except Exception as e:
                print(f"Warning: Could not get admin name for id {admin_id}: {e}")
        
        # room_id를 room 번호로 변환
        room_id = note.get('room_id', '')
        room_number = ''
        if room_id:
            try:
                room_data = self.get_room(room_id)
                if room_data:
                    room_number = room_data.get('room_number', '')
            except Exception as e:
                print(f"Warning: Could not get room number for id {room_id}: {e}")
        
        # 데이터 매핑 (다양한 헤더 이름 지원)
        # Room Number 또는 room_id
        for key in ['room_number', 'room_id', 'room number', 'roomnumber']:
            if key in header_map:
                row[header_map[key]] = room_number if room_number else str(room_id)
                break
        
        # Name 또는 admin_id 또는 role
        for key in ['name', 'admin_id', 'admin id', 'adminid', 'role']:
            if key in header_map:
                row[header_map[key]] = admin_name if admin_name else str(admin_id)
                break
        
        # Note Type 또는 note_type
        for key in ['note_type', 'note type', 'notetype']:
            if key in header_map:
                row[header_map[key]] = str(note.get('note_type', ''))
                break
        
        # Title
        if 'title' in header_map:
            row[header_map['title']] = str(note.get('title', ''))
        
        # Description
        if 'description' in header_map:
            row[header_map['description']] = str(note.get('description', ''))
        
        # Progress
        if 'progress' in header_map:
            row[header_map['progress']] = str(note.get('progress', ''))
        
        # Reservation ID
        for key in ['reservation_id', 'reservation id', 'reservationid']:
            if key in header_map:
                row[header_map[key]] = str(note.get('reservation_id', ''))
                break
        
        # Status
        if 'status' in header_map:
            row[header_map['status']] = str(note.get('status', 'pending'))
        
        # Created At
        for key in ['created_at', 'created at', 'createdat']:
            if key in header_map:
                row[header_map[key]] = str(note.get('created_at', ''))
                break
        
        # Completed At
        for key in ['completed_at', 'completed at', 'completedat']:
            if key in header_map:
                row[header_map[key]] = str(note.get('completed_at', ''))
                break
        
        # id는 자동 생성 (행 번호)
        note['id'] = str(len(data))
        self._append_to_sheet("note", [row])
        return note
    
    def update_note_progress(self, note_id: str, progress: str):
        """노트 progress 업데이트"""
        data = self._read_sheet("note")
        if len(data) < 2:
            return
        
        headers = data[0]
        header_map = {h.lower(): i for i, h in enumerate(headers)}
        
        try:
            progress_col = header_map.get('progress')
            if progress_col is None:
                print("Progress column not found in note sheet")
                return
            
            # note_id는 행 번호로 사용
            row_index = int(note_id) + 1  # 헤더 제외하고 1부터 시작
            
            if row_index <= len(data):
                # range_name에는 시트 이름을 포함하지 않음 (_write_sheet에서 추가됨)
                range_name = f"{chr(65 + progress_col)}{row_index}"
                self._write_sheet("note", [[progress]], range_name)
        except (ValueError, IndexError) as e:
            print(f"Error updating note progress: {e}")
    
    def get_notes_by_progress(self, progress: str = None) -> List[Dict]:
        """progress별 노트 조회 (progress가 None이면 progress가 없는 노트만)"""
        notes = self.get_notes()
        if progress is None:
            # progress가 비어있거나 없는 노트만
            return [n for n in notes if not n.get('progress') or n.get('progress').strip() == '']
        else:
            return [n for n in notes if n.get('progress', '').strip() == progress]
    
    def get_urgent_notes(self) -> List[Dict]:
        """긴급 메모 조회"""
        notes = self.get_notes()
        return [n for n in notes if n.get('note_type') == 'urgent' and (not n.get('progress') or n.get('progress').strip() == '')]
    
    def get_after_checkout_notes(self) -> List[Dict]:
        """체크아웃 후 처리 메모 조회"""
        notes = self.get_notes()
        return [n for n in notes if n.get('note_type') == 'after_checkout' and (not n.get('progress') or n.get('progress').strip() == '')]

