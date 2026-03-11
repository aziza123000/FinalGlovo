# review_api.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.models import Review
from mysite.database.schema import ReviewInputSchema, ReviewOutSchema

review_router = APIRouter(prefix='/reviews', tags=['Reviews'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@review_router.post('/', response_model=ReviewOutSchema)
async def create_review(review: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db = Review(**review.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.get('/', response_model=List[ReviewOutSchema])
async def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()

@review_router.get('/{review_id}', response_model=ReviewOutSchema)
async def get_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail='Отзыв не найден')
    return review_db

@review_router.put('/{review_id}', response_model=ReviewOutSchema)
async def update_review(review_id: int, review: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail='Отзыв не найден')
    for key, value in review.dict().items():
        setattr(review_db, key, value)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.delete('/{review_id}')
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail='Отзыв не найден')
    db.delete(review_db)
    db.commit()
    return {'message': 'Отзыв удален'}