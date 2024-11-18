from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Message
from app.database import get_db
from sqlalchemy.future import select
from typing import List
from fastapi import Depends, HTTPException, status
from app.auth.utils import get_user_from_token
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from fastapi.security import OAuth2PasswordBearer
from app.chat.schemas import MessageRequest
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    username = get_user_from_token(token) 
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    user = await db.execute(select(User).filter(User.username == username))
    user = user.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.post("/send_message")
async def send_message(message: MessageRequest, db: AsyncSession = Depends(get_db)):
    print(f"Received message with sender_id: {message.sender_id}, receiver_id: {message.receiver_id}, content: {message.content}")
    
    new_message = Message(sender_id=message.sender_id, receiver_id=message.receiver_id, content=message.content, timestamp=datetime.now())

    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)

    return {"message": "Message sent successfully", "content": message.content}

@router.get("/messages/{user_id}")
async def get_messages(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    messages = await db.execute(
        select(Message).filter(
            (Message.sender_id == current_user.id) & (Message.receiver_id == user_id) |
            (Message.sender_id == user_id) & (Message.receiver_id == current_user.id)
        ).order_by(Message.timestamp)
    )
    return messages.scalars().all()

@router.get("/users", response_model=None)
async def get_all_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = await db.execute(select(User).filter(User.id != current_user.id))
    return users.scalars().all()