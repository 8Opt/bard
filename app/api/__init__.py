from fastapi import APIRouter

from app.api.routes import (
    chat_router,
    auth_router
)

api_router = APIRouter()

api_router.include_router(chat_router, prefix="/chat", tags=["CHAT"])
api_router.include_router(auth_router, prefix="/auth", tags=["AUTH"])
