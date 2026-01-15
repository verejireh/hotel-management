"""
Google Sheets에서 MySQL로 데이터 마이그레이션 스크립트
"""
import sys
from app.sheets import GoogleSheetsDB as OldDB
from app.db import MySQLDB as NewDB
from app.database import Base, engine

def migrate_data():
    """Google Sheets 데이터를 MySQL로 마이그레이션"""
    print("=" * 50)
    print("Starting data migration from Google Sheets to MySQL...")
    print("=" * 50)
    
    # 데이터베이스 초기화
    print("\n[1/7] Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    old_db = OldDB()
    new_db = NewDB()
    
    try:
        # 1. Customers 마이그레이션
        print("\n[2/6] Migrating customers...")
        customers = old_db.get_customers()
        for customer in customers:
            try:
                new_db.create_customer(customer)
            except Exception as e:
                print(f"  Error migrating customer {customer.get('id')}: {e}")
        print(f"  Migrated {len(customers)} customers")
        
        # 2. Booking Platforms 마이그레이션
        print("\n[3/7] Migrating booking platforms...")
        platforms = old_db.get_platforms()
        for platform in platforms:
            try:
                new_db.create_platform(platform)
            except Exception as e:
                print(f"  Error migrating platform {platform.get('id')}: {e}")
        print(f"  Migrated {len(platforms)} platforms")
        
        # 3. Rooms 마이그레이션
        print("\n[4/7] Migrating rooms...")
        rooms = old_db.get_rooms()
        for room in rooms:
            try:
                new_db.create_room(room)
            except Exception as e:
                print(f"  Error migrating room {room.get('id')}: {e}")
        print(f"  Migrated {len(rooms)} rooms")
        
        # 4. Admins 마이그레이션
        print("\n[5/7] Migrating admins...")
        admins = old_db.get_admins()
        for admin in admins:
            try:
                new_db.create_admin(admin)
            except Exception as e:
                print(f"  Error migrating admin {admin.get('id')}: {e}")
        print(f"  Migrated {len(admins)} admins")
        
        # 5. Reservations 마이그레이션
        print("\n[6/7] Migrating reservations...")
        reservations = old_db.get_reservations()
        migrated_count = 0
        for reservation in reservations:
            try:
                # customer_id를 이름에서 ID로 변환 (필요시)
                customer_id = reservation.get('customer_id', '')
                if isinstance(customer_id, str) and not customer_id.isdigit():
                    customers_list = new_db.get_customers()
                    for c in customers_list:
                        if str(c.get('id')) == customer_id or c.get('name') == customer_id:
                            customer_id = c.get('id')
                            break
                
                # room_id를 room_number에서 ID로 변환
                room_id = reservation.get('room_id', '')
                rooms_list = new_db.get_rooms()
                room_found = None
                for r in rooms_list:
                    if str(r.get('id')) == str(room_id) or r.get('room_number') == str(room_id):
                        room_found = r.get('id')
                        break
                
                # platform_id를 이름에서 ID로 변환 (필요시)
                platform_id = reservation.get('platform_id', '')
                if isinstance(platform_id, str) and not platform_id.isdigit():
                    platforms_list = new_db.get_platforms()
                    for p in platforms_list:
                        if str(p.get('id')) == platform_id or p.get('name') == platform_id:
                            platform_id = p.get('id')
                            break
                
                if room_found:
                    reservation['customer_id'] = int(customer_id) if customer_id else 0
                    reservation['room_id'] = int(room_found)
                    reservation['platform_id'] = int(platform_id) if platform_id else 0
                    new_db.create_reservation(reservation)
                    migrated_count += 1
                else:
                    print(f"  Skipping reservation {reservation.get('id')}: room not found")
            except Exception as e:
                print(f"  Error migrating reservation {reservation.get('id')}: {e}")
        print(f"  Migrated {migrated_count}/{len(reservations)} reservations")
        
        # 6. Notes 마이그레이션
        print("\n[7/7] Migrating notes...")
        notes = old_db.get_notes()
        for note in notes:
            try:
                # admin_id를 이름에서 ID로 변환
                admin_name = note.get('admin_id', '')
                admins_list = new_db.get_admins()
                admin_id = None
                for a in admins_list:
                    if a.get('name') == admin_name:
                        admin_id = a.get('id')
                        break
                
                if admin_id:
                    note['admin_id'] = admin_id
                    new_db.create_note(note)
            except Exception as e:
                print(f"  Error migrating note {note.get('id')}: {e}")
        print(f"  Migrated {len(notes)} notes")
        
        print("\n" + "=" * 50)
        print("Migration completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n[ERROR] Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        new_db.db.close()
    
    return True

if __name__ == "__main__":
    success = migrate_data()
    sys.exit(0 if success else 1)

