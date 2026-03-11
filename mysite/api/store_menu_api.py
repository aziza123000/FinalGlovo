from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.models import StoreMenu
from mysite.database.schema import StoreMenuInputSchema, StoreMenuOutSchema

store_menu_router = APIRouter(prefix='/store/menu', tags=['Store_Menu'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@store_menu_router.post('/', response_model=StoreMenuOutSchema)
async def create_menu(menu: StoreMenuInputSchema, db: Session = Depends(get_db)):
    menu_db = StoreMenu(**menu.dict())
    db.add(menu_db)
    db.commit()
    db.refresh(menu_db)
    return menu_db

@store_menu_router.get('/', response_model=List[StoreMenuOutSchema])
async def get_menus(db: Session = Depends(get_db)):
    return db.query(StoreMenu).all()

@store_menu_router.get('/{store_menu_id}', response_model=StoreMenuOutSchema)
async def get_menu(store_menu_id: int, db: Session = Depends(get_db)):
    menu_db = db.query(StoreMenu).filter(StoreMenu.id == store_menu_id).first()
    if not menu_db:
        raise HTTPException(status_code=404, detail='Меню не найдено')
    return menu_db

@store_menu_router.put('/{store_menu_id}', response_model=StoreMenuOutSchema)
async def update_menu(store_menu_id: int, menu: StoreMenuInputSchema, db: Session = Depends(get_db)):
    menu_db = db.query(StoreMenu).filter(StoreMenu.id == store_menu_id).first()
    if not menu_db:
        raise HTTPException(status_code=404, detail='Меню не найдено')
    for key, value in menu.dict().items():
        setattr(menu_db, key, value)
    db.commit()
    db.refresh(menu_db)
    return menu_db

@store_menu_router.delete('/{store_menu_id}')
async def delete_menu(store_menu_id: int, db: Session = Depends(get_db)):
    menu_db = db.query(StoreMenu).filter(StoreMenu.id == store_menu_id).first()
    if not menu_db:
        raise HTTPException(status_code=404, detail='Меню не найдено')
    db.delete(menu_db)
    db.commit()
    return {'message': 'Меню удалено'}