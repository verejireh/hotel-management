from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models import Admin
from app.db import MySQLDB

router = APIRouter(prefix="/api/admins", tags=["admins"])


def get_db():
    return MySQLDB()


@router.get("/", response_model=List[Admin])
async def get_admins(db: MySQLDB = Depends(get_db)):
    """모든 관리자 조회"""
    admins_data = db.get_admins()
    admins = []
    for a in admins_data:
        try:
            admin = Admin(
                id=a.get('id'),
                name=a.get('name', ''),
                email=a.get('email') if a.get('email') else None,
                phone=a.get('phone') if a.get('phone') else None,
                role=a.get('role') if a.get('role') else None,
                is_active=True  # 기본값
            )
            admins.append(admin)
        except Exception as e:
            print(f"Error parsing admin: {e}")
            continue
    return admins


@router.get("/{admin_id}", response_model=Admin)
async def get_admin(admin_id: str, db: MySQLDB = Depends(get_db)):
    """관리자 상세 조회"""
    admin_data = db.get_admin(admin_id)
    if not admin_data:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    return Admin(
        id=admin_data.get('id'),
        name=admin_data.get('name', ''),
        email=admin_data.get('email'),
        phone=admin_data.get('phone'),
        role=admin_data.get('role'),
        is_active=admin_data.get('is_active', 'true').lower() == 'true' if admin_data.get('is_active') else True
    )


@router.post("/", response_model=Admin)
async def create_admin(admin: Admin, db: MySQLDB = Depends(get_db)):
    """새 관리자 생성"""
    try:
        admin_dict = admin.dict(exclude={'id', 'is_active'})
        new_admin = db.create_admin(admin_dict)
        
        return Admin(
            id=new_admin.get('id'),
            name=new_admin.get('name', ''),
            email=new_admin.get('email'),
            phone=new_admin.get('phone'),
            role=new_admin.get('role'),
            is_active=True
        )
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Failed to create admin: {str(e)}")


@router.delete("/{admin_id}")
async def delete_admin(admin_id: str, db: MySQLDB = Depends(get_db)):
    """관리자 삭제"""
    try:
        # admin이 존재하는지 확인
        admin_data = db.get_admin(admin_id)
        if not admin_data:
            raise HTTPException(status_code=404, detail="Admin not found")
        
        # admin 삭제
        db.delete_admin(admin_id)
        return {"message": "Admin deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete admin: {str(e)}")

