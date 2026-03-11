from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from mysite.database.db import SessionLocal
from mysite.models import UserProfile
from mysite.database.schema import UserProfileInputSchema, UserProfileOutSchema, UserLoginSchema
from passlib.context import CryptContext

auth_router = APIRouter(prefix='/auth', tags=['Auth'])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@auth_router.post('/register/', response_model=dict)
async def register(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    email_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()

    if user_db or email_db:
        raise HTTPException(status_code=400, detail='Такой username или email уже существует')

    new_user = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
        role=user.role,
        date_registered=user.date_registered
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'message': 'Регистрация прошла успешно'}


@auth_router.post('/login/', response_model=dict)
async def login(user: UserLoginSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if not user_db or not verify_password(user.password, user_db.password):
        raise HTTPException(status_code=401, detail='Неверный username или пароль')
    return {'message': 'Вход выполнен успешно'}


@auth_router.post('/logout/', response_model=dict)
async def logout():
    return {'message': 'Вы вышли из системы'}