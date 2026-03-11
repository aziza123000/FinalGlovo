from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.models import CourierProfile
from mysite.database.schema import CourierProfileInputSchema, CourierProfileOutSchema

courier_router = APIRouter(prefix='/courier/product', tags=['Courier_Product'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@courier_router.post('/', response_model=CourierProfileOutSchema)
async def create_courier(courier: CourierProfileInputSchema, db: Session = Depends(get_db)):
    courier_db = CourierProfile(**courier.dict())
    db.add(courier_db)
    db.commit()
    db.refresh(courier_db)
    return courier_db

@courier_router.get('/', response_model=List[CourierProfileOutSchema])
async def get_couriers(db: Session = Depends(get_db)):
    return db.query(CourierProfile).all()

@courier_router.get('/{courier_product_id}', response_model=CourierProfileOutSchema)
async def get_courier(courier_product_id: int, db: Session = Depends(get_db)):
    courier_db = db.query(CourierProfile).filter(CourierProfile.id == courier_product_id).first()
    if not courier_db:
        raise HTTPException(status_code=404, detail='Курьер не найден')
    return courier_db

@courier_router.put('/{courier_product_id}', response_model=CourierProfileOutSchema)
async def update_courier(courier_product_id: int, courier: CourierProfileInputSchema, db: Session = Depends(get_db)):
    courier_db = db.query(CourierProfile).filter(CourierProfile.id == courier_product_id).first()
    if not courier_db:
        raise HTTPException(status_code=404, detail='Курьер не найден')
    for key, value in courier.dict().items():
        setattr(courier_db, key, value)
    db.commit()
    db.refresh(courier_db)
    return courier_db

@courier_router.delete('/{courier_product_id}')
async def delete_courier(courier_product_id: int, db: Session = Depends(get_db)):
    courier_db = db.query(CourierProfile).filter(CourierProfile.id == courier_product_id).first()
    if not courier_db:
        raise HTTPException(status_code=404, detail='Курьер не найден')
    db.delete(courier_db)
    db.commit()
    return {'message': 'Курьер удален'}