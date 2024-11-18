from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.auth.schemas import UserCreate, UserOut
from app.auth.utils import hash_password
from app.database import get_db
from app.auth.utils import verify_password, create_access_token
from sqlalchemy.future import select
from typing import List

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if the user already exists
    existing_user = await db.execute(
        User.__table__.select().where(User.username == user.username)
    )
    if existing_user.scalar():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Hash password and save the user
    hashed_pwd = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_pwd)
    db.add(new_user)
    await db.commit()
    return new_user

# Correct way to fetch a single user by username
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()

@router.post("/login")
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Fetch the user by username
    db_user = await get_user_by_username(db, user.username)

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users", response_model=List[User])
async def get_all_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = await db.execute(select(User).filter(User.id != current_user.id))
    return users.scalars().all()