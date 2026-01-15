from fastapi import APIRouter, Depends
from typing import List
from app.db import MySQLDB

router = APIRouter(prefix="/api/cleaning", tags=["cleaning"])


def get_db():
    return MySQLDB()


@router.get("/rooms")
async def get_cleaning_rooms(db: MySQLDB = Depends(get_db)):
    """청소가 필요한 방 목록"""
    rooms_data = db.get_rooms()
    
    cleaning_rooms = []
    for room_data in rooms_data:
        if room_data.get('status') == 'cleaning':
            from app.models import Room
            try:
                room = Room(
                    id=room_data.get('id'),
                    room_number=room_data.get('room_number', ''),
                    room_type=room_data.get('room_type', ''),
                    max_guests=int(room_data.get('max_guests', 0)),
                    price_per_night=float(room_data.get('price_per_night', 0)),
                    status=room_data.get('status', 'cleaning')
                )
                cleaning_rooms.append(room)
            except:
                continue
    
    return {
        "cleaning_rooms": cleaning_rooms,
        "count": len(cleaning_rooms)
    }


@router.post("/complete/{room_id}")
async def complete_cleaning(room_id: str, db: MySQLDB = Depends(get_db)):
    """청소 완료 처리"""
    db.update_room_status(room_id, "available")
    
    room_data = db.get_room(room_id)
    if not room_data:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Room not found")
    
    from app.models import Room
    return Room(
        id=room_data.get('id'),
        room_number=room_data.get('room_number', ''),
        room_type=room_data.get('room_type', ''),
        max_guests=int(room_data.get('max_guests', 0)),
        price_per_night=float(room_data.get('price_per_night', 0)),
        status="available"
    )






