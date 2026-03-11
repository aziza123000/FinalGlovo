from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.models import Address
from mysite.database.schema import AddressInputSchema, AddressOutSchema

address_router = APIRouter(prefix='/address', tags=['Address'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@address_router.post('/', response_model=AddressOutSchema)
async def create_address(address: AddressInputSchema, db: Session = Depends(get_db)):
    address_db = Address(**address.dict())
    db.add(address_db)
    db.commit()
    db.refresh(address_db)
    return address_db

@address_router.get('/', response_model=List[AddressOutSchema])
async def get_addresses(db: Session = Depends(get_db)):
    return db.query(Address).all()

@address_router.get('/{address_id}', response_model=AddressOutSchema)
async def get_address(address_id: int, db: Session = Depends(get_db)):
    address_db = db.query(Address).filter(Address.id == address_id).first()
    if not address_db:
        raise HTTPException(status_code=404, detail='Адрес не найден')
    return address_db

@address_router.put('/{address_id}', response_model=AddressOutSchema)
async def update_address(address_id: int, address: AddressInputSchema, db: Session = Depends(get_db)):
    address_db = db.query(Address).filter(Address.id == address_id).first()
    if not address_db:
        raise HTTPException(status_code=404, detail='Адрес не найден')
    for key, value in address.dict().items():
        setattr(address_db, key, value)
    db.commit()
    db.refresh(address_db)
    return address_db

@address_router.delete('/{address_id}')
async def delete_address(address_id: int, db: Session = Depends(get_db)):
    address_db = db.query(Address).filter(Address.id == address_id).first()
    if not address_db:
        raise HTTPException(status_code=404, detail='Адрес не найден')
    db.delete(address_db)
    db.commit()
    return {'message': 'Адрес удален'}