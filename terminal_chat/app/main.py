from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.chat.routes import router as chat_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
