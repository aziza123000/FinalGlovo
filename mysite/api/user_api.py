from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.models import UserProfile
from mysite.database.schema import UserProfileInputSchema, UserProfileOutSchema

user_router = APIRouter(prefix='/users', tags=['Users'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.post('/', response_model=UserProfileOutSchema)
async def create_user(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = UserProfile(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@user_router.get('/', response_model=List[UserProfileOutSchema])
async def get_users(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()

@user_router.get('/{user_id}', response_model=UserProfileOutSchema)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return user_db

@user_router.put('/{user_id}', response_model=UserProfileOutSchema)
async def update_user(user_id: int, user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    for key, value in user.dict().items():
        setattr(user_db, key, value)
    db.commit()
    db.refresh(user_db)
    return user_db

@user_router.delete('/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    db.delete(user_db)
    db.commit()
    return {'message': 'Пользователь удален'}