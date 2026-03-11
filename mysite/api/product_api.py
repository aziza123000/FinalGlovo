# product_api.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.models import Product
from mysite.database.schema import ProductInputSchema, ProductOutSchema

product_router = APIRouter(prefix='/products', tags=['Products'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_router.post('/', response_model=ProductOutSchema)
async def create_product(product: ProductInputSchema, db: Session = Depends(get_db)):
    product_db = Product(**product.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db

@product_router.get('/', response_model=List[ProductOutSchema])
async def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@product_router.get('/{product_id}', response_model=ProductOutSchema)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Продукт не найден')
    return product_db

@product_router.put('/{product_id}', response_model=ProductOutSchema)
async def update_product(product_id: int, product: ProductInputSchema, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Продукт не найден')
    for key, value in product.dict().items():
        setattr(product_db, key, value)
    db.commit()
    db.refresh(product_db)
    return product_db

@product_router.delete('/{product_id}')
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Продукт не найден')
    db.delete(product_db)
    db.commit()
    return {'message': 'Продукт удален'}