from fastapi import APIRouter, Depends
from typing import List
from app.models import Room
from app.db import MySQLDB

router = APIRouter(prefix="/api/rooms", tags=["rooms"])


def get_db():
    return MySQLDB()


@router.get("/", response_model=List[Room])
async def get_rooms(db: MySQLDB = Depends(get_db)):
    """모든 방 조회"""
    rooms_data = db.get_rooms()
    rooms = []
    for r in rooms_data:
        try:
            room = Room(
                id=r.get('id'),
                room_number=r.get('room_number', ''),
                room_type=r.get('room_type', ''),
                max_guests=int(r.get('max_guests', 0)),
                price_per_night=float(r.get('price_per_night', 0)),
                status=r.get('status', 'available')
            )
            rooms.append(room)
        except Exception as e:
            print(f"Error parsing room: {e}")
            continue
    return rooms


@router.get("/{room_id}", response_model=Room)
async def get_room(room_id: str, db: MySQLDB = Depends(get_db)):
    """방 상세 조회"""
    room_data = db.get_room(room_id)
    if not room_data:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Room not found")
    
    return Room(
        id=room_data.get('id'),
        room_number=room_data.get('room_number', ''),
        room_type=room_data.get('room_type', ''),
        max_guests=int(room_data.get('max_guests', 0)),
        price_per_night=float(room_data.get('price_per_night', 0)),
        status=room_data.get('status', 'available')
    )






