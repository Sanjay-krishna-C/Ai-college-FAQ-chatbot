from fastapi import APIRouter
from app.api.routes import health, chat, rag

api_router = APIRouter(prefix="/api")

# Register route modules under /api
api_router.include_router(health.router)
api_router.include_router(chat.router)
api_router.include_router(rag.router)
