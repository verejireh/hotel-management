from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime
from app.models import RoomNote, RoomNoteCreate
from app.db import MySQLDB

router = APIRouter(prefix="/api/room-notes", tags=["room-notes"])


def get_db():
    return MySQLDB()


@router.get("/", response_model=List[RoomNote])
async def get_room_notes(room_id: str = None, progress: str = None, db: MySQLDB = Depends(get_db)):
    """모든 노트 조회 (room_id, progress 필터 옵션)"""
    import sys
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"[API] get_room_notes called with room_id={room_id}, progress={progress}")
    print(f"[API] get_room_notes called with room_id={room_id}, progress={progress}", file=sys.stderr, flush=True)
    print(f"[API] get_room_notes called with room_id={room_id}, progress={progress}", flush=True)
    
    # progress 파라미터 처리
    import sys
    if progress is not None and progress != '':
        # 특정 progress 값으로 필터링
        notes_data = db.get_notes_by_progress(progress)
        print(f"[API] Filtered by progress '{progress}': {len(notes_data)} notes found", file=sys.stderr, flush=True)
        print(f"[API] Filtered by progress '{progress}': {len(notes_data)} notes found", flush=True)
    elif progress == '':
        # 빈 문자열이면 progress가 없는 노트만
        notes_data = db.get_notes_by_progress(None)
        print(f"[API] Filtered by no progress: {len(notes_data)} notes found", file=sys.stderr, flush=True)
        print(f"[API] Filtered by no progress: {len(notes_data)} notes found", flush=True)
    else:
        # progress가 None이면 모든 노트 반환 (progress 필터 없이)
        notes_data = db.get_notes()
        print(f"[API] All notes (no filter): {len(notes_data)} notes found", file=sys.stderr, flush=True)
        print(f"[API] All notes (no filter): {len(notes_data)} notes found", flush=True)
    
    if room_id:
        notes_data = [n for n in notes_data if n.get('room_id') == room_id]
        print(f"Filtered by room_id '{room_id}': {len(notes_data)} notes found")
    
    notes = []
    import sys
    print(f"[API DEBUG] Processing {len(notes_data)} notes_data items", file=sys.stderr, flush=True)
    print(f"[API DEBUG] Processing {len(notes_data)} notes_data items", flush=True)
    
    if len(notes_data) > 0:
        print(f"[API DEBUG] First notes_data item: {notes_data[0]}", file=sys.stderr, flush=True)
        print(f"[API DEBUG] First notes_data item: {notes_data[0]}", flush=True)
    
    for n in notes_data:
        try:
            print(f"[API DEBUG] Processing note: id={n.get('id')}, title={n.get('title')}, desc={n.get('description')}", file=sys.stderr, flush=True)
            # 필수 필드 검증
            if not n.get('title') and not n.get('description'):
                print(f"[API] Skipping note {n.get('id')}: no title or description", file=sys.stderr, flush=True)
                print(f"[API] Skipping note {n.get('id')}: no title or description", flush=True)
                continue
                
            # RoomNote 모델 생성 시 에러 처리
            try:
                # created_at과 completed_at이 빈 문자열이면 None으로 변환
                created_at = n.get('created_at')
                if created_at == '' or created_at is None:
                    created_at = None
                
                completed_at = n.get('completed_at')
                if completed_at == '' or completed_at is None:
                    completed_at = None
                
                note = RoomNote(
                    id=n.get('id'),
                    room_id=str(n.get('room_id', '')),
                    admin_id=str(n.get('admin_id', '')),
                    note_type=str(n.get('note_type', '')),
                    title=str(n.get('title', '')),
                    description=str(n.get('description', '')),
                    status=str(n.get('status', 'pending')),
                    created_at=created_at,
                    completed_at=completed_at,
                    reservation_id=n.get('reservation_id') if n.get('reservation_id') else None,
                    progress=n.get('progress') if n.get('progress') else None
                )
                notes.append(note)
                print(f"[API] Added note {note.id}: title='{note.title[:30] if note.title else ''}...'", flush=True)
            except Exception as model_error:
                print(f"[API ERROR] Failed to create RoomNote model: {model_error}", file=sys.stderr, flush=True)
                print(f"[API ERROR] Failed to create RoomNote model: {model_error}", flush=True)
                print(f"[API ERROR] Note dict: {n}", flush=True)
                import traceback
                traceback.print_exc()
                continue
        except Exception as e:
            print(f"[API ERROR] Error parsing room note: {e}", file=sys.stderr, flush=True)
            print(f"[API ERROR] Error parsing room note: {e}", flush=True)
            print(f"[API ERROR] Note data: {n}", flush=True)
            import traceback
            traceback.print_exc()
            continue
    
    print(f"[API] Returning {len(notes)} notes", file=sys.stderr, flush=True)
    print(f"[API] Returning {len(notes)} notes", flush=True)
    
    # 디버깅: 실제 데이터 확인
    if len(notes_data) > 0 and len(notes) == 0:
        print(f"[API DEBUG] notes_data has {len(notes_data)} items but notes is empty", file=sys.stderr, flush=True)
        print(f"[API DEBUG] First notes_data item: {notes_data[0] if notes_data else 'None'}", file=sys.stderr, flush=True)
    
    return notes


@router.get("/urgent")
async def get_urgent_notes(db: MySQLDB = Depends(get_db)):
    """긴급 메모 조회"""
    notes_data = db.get_urgent_notes()
    notes = []
    for n in notes_data:
        try:
            note = RoomNote(
                id=n.get('id'),
                room_id=n.get('room_id', ''),
                admin_id=n.get('admin_id', ''),
                note_type=n.get('note_type', ''),
                title=n.get('title', ''),
                description=n.get('description', ''),
                status=n.get('status', 'pending'),
                created_at=n.get('created_at'),
                completed_at=n.get('completed_at'),
                reservation_id=n.get('reservation_id'),
                progress=n.get('progress')
            )
            notes.append(note)
        except:
            continue
    
    return {
        "urgent_notes": notes,
        "count": len(notes)
    }


@router.get("/after-checkout")
async def get_after_checkout_notes(db: MySQLDB = Depends(get_db)):
    """체크아웃 후 처리 메모 조회"""
    notes_data = db.get_after_checkout_notes()
    notes = []
    for n in notes_data:
        try:
            note = RoomNote(
                id=n.get('id'),
                room_id=n.get('room_id', ''),
                admin_id=n.get('admin_id', ''),
                note_type=n.get('note_type', ''),
                title=n.get('title', ''),
                description=n.get('description', ''),
                status=n.get('status', 'pending'),
                created_at=n.get('created_at'),
                completed_at=n.get('completed_at'),
                reservation_id=n.get('reservation_id'),
                progress=n.get('progress')
            )
            notes.append(note)
        except:
            continue
    
    return {
        "after_checkout_notes": notes,
        "count": len(notes)
    }


@router.get("/alerts")
async def get_all_alerts(progress: str = None, db: MySQLDB = Depends(get_db)):
    """모든 알람 조회 (긴급 + 체크아웃 후, progress 필터 옵션)"""
    # progress 필터 적용
    if progress:
        all_notes = db.get_notes_by_progress(progress)
    else:
        # progress가 None이면 progress가 없는 노트만
        all_notes = db.get_notes_by_progress(None)
    
    urgent_notes = []
    after_checkout_notes = []
    
    for n in all_notes:
        try:
            note = RoomNote(
                id=n.get('id'),
                room_id=n.get('room_id', ''),
                admin_id=n.get('admin_id', ''),
                note_type=n.get('note_type', ''),
                title=n.get('title', ''),
                description=n.get('description', ''),
                status=n.get('status', 'pending'),
                created_at=n.get('created_at'),
                completed_at=n.get('completed_at'),
                reservation_id=n.get('reservation_id'),
                progress=n.get('progress')
            )
            
            if n.get('note_type') == 'urgent':
                urgent_notes.append(note)
            elif n.get('note_type') == 'after_checkout':
                after_checkout_notes.append(note)
        except:
            continue
    
    return {
        "urgent_notes": urgent_notes,
        "after_checkout_notes": after_checkout_notes,
        "total_count": len(urgent_notes) + len(after_checkout_notes)
    }


@router.post("/", response_model=RoomNote)
async def create_room_note(note: RoomNoteCreate, db: MySQLDB = Depends(get_db)):
    """새 노트 생성 (note 시트에 저장)"""
    try:
        note_dict = note.dict()
        note_dict['status'] = 'pending'
        note_dict['created_at'] = str(datetime.now())
        note_dict['completed_at'] = ''
        
        new_note = db.create_note(note_dict)
        
        return RoomNote(
            id=new_note.get('id'),
            room_id=new_note.get('room_id', ''),
            admin_id=new_note.get('admin_id', ''),
            note_type=new_note.get('note_type', ''),
            title=new_note.get('title', ''),
            description=new_note.get('description', ''),
            status=new_note.get('status', 'pending'),
            created_at=new_note.get('created_at'),
            completed_at=new_note.get('completed_at'),
            reservation_id=new_note.get('reservation_id'),
            progress=new_note.get('progress')
        )
    except Exception as e:
        import traceback
        error_detail = str(e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create note: {error_detail}")


@router.post("/{note_id}/complete")
async def complete_room_note(note_id: str, db: MySQLDB = Depends(get_db)):
    """노트 완료 처리"""
    note_data = db.get_note(note_id)
    if not note_data:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.update_note_progress(note_id, 'finished')
    
    updated_note = db.get_note(note_id)
    return RoomNote(
        id=updated_note.get('id'),
        room_id=updated_note.get('room_id', ''),
        admin_id=updated_note.get('admin_id', ''),
        note_type=updated_note.get('note_type', ''),
        title=updated_note.get('title', ''),
        description=updated_note.get('description', ''),
        status='completed',
        created_at=updated_note.get('created_at'),
        completed_at=updated_note.get('completed_at'),
        reservation_id=updated_note.get('reservation_id'),
        progress=updated_note.get('progress')
    )


@router.put("/{note_id}/progress")
async def update_note_progress(note_id: str, progress: str = Query(..., description="Progress value"), db: MySQLDB = Depends(get_db)):
    """노트 progress 업데이트"""
    if progress not in ['confirm', 'In progress', 'finished', '']:
        raise HTTPException(status_code=400, detail="Invalid progress value. Must be 'confirm', 'In progress', 'finished', or empty string")
    
    note_data = db.get_note(note_id)
    if not note_data:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.update_note_progress(note_id, progress)
    
    updated_note = db.get_note(note_id)
    return RoomNote(
        id=updated_note.get('id'),
        room_id=updated_note.get('room_id', ''),
        admin_id=updated_note.get('admin_id', ''),
        note_type=updated_note.get('note_type', ''),
        title=updated_note.get('title', ''),
        description=updated_note.get('description', ''),
        status=updated_note.get('status', 'pending'),
        created_at=updated_note.get('created_at'),
        completed_at=updated_note.get('completed_at'),
        reservation_id=updated_note.get('reservation_id'),
        progress=updated_note.get('progress')
    )

