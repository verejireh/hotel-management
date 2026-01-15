from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from app.models import Customer
from app.db import MySQLDB

router = APIRouter(prefix="/api/customers", tags=["customers"])


def get_db():
    return MySQLDB()


@router.get("/", response_model=List[Customer])
async def get_customers(db: MySQLDB = Depends(get_db)):
    """모든 고객 조회"""
    customers_data = db.get_customers()
    customers = []
    for c in customers_data:
        try:
            customer = Customer(
                id=c.get('id'),
                name=c.get('name', ''),
                email=c.get('email'),
                phone=c.get('phone'),
                nationality=c.get('nationality')
            )
            customers.append(customer)
        except Exception as e:
            print(f"Error parsing customer: {e}")
            continue
    return customers


@router.get("/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str, db: MySQLDB = Depends(get_db)):
    """고객 상세 조회"""
    customer_data = db.get_customer(customer_id)
    if not customer_data:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return Customer(
        id=customer_data.get('id'),
        name=customer_data.get('name', ''),
        email=customer_data.get('email'),
        phone=customer_data.get('phone'),
        nationality=customer_data.get('nationality')
    )


@router.get("/{customer_id}/reservations")
async def get_customer_reservations(customer_id: str, db: MySQLDB = Depends(get_db)):
    """고객의 예약 이력 조회"""
    from app.utils import reservation_dict_to_model
    
    reservations_data = db.get_reservations()
    customer_reservations = []
    
    for res_data in reservations_data:
        if res_data.get('customer_id') == customer_id:
            try:
                reservation = reservation_dict_to_model(res_data)
                customer_reservations.append(reservation)
            except:
                continue
    
    return {
        "customer_id": customer_id,
        "reservations": customer_reservations
    }


@router.post("/", response_model=Customer)
async def create_customer(customer: Customer, db: MySQLDB = Depends(get_db)):
    """새 고객 생성"""
    customer_dict = customer.dict(exclude={'id'})
    new_customer = db.create_customer(customer_dict)
    
    return Customer(
        id=new_customer.get('id'),
        name=new_customer.get('name', ''),
        email=new_customer.get('email'),
        phone=new_customer.get('phone'),
        nationality=new_customer.get('nationality')
    )






