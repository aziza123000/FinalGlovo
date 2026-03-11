# category_api.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.models import Category
from mysite.database.schema import CategoryInputSchema, CategoryOutSchema

category_router = APIRouter(prefix='/categories', tags=['Categories'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@category_router.post('/', response_model=CategoryOutSchema)
async def create_category(category: CategoryInputSchema, db: Session = Depends(get_db)):
    category_db = Category(**category.dict())
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db

@category_router.get('/', response_model=List[CategoryOutSchema])
async def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@category_router.get('/{category_id}', response_model=CategoryOutSchema)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=404, detail='Категория не найдена')
    return category_db

@category_router.put('/{category_id}', response_model=CategoryOutSchema)
async def update_category(category_id: int, category: CategoryInputSchema, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=404, detail='Категория не найдена')
    for key, value in category.dict().items():
        setattr(category_db, key, value)
    db.commit()
    db.refresh(category_db)
    return category_db

@category_router.delete('/{category_id}')
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=404, detail='Категория не найдена')
    db.delete(category_db)
    db.commit()
    return {'message': 'Категория удалена'}