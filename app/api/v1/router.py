from fastapi import APIRouter
from app.api.v1.endpoints import enrich, users # <--- Añadir importación

api_router = APIRouter()

api_router.include_router(enrich.router, prefix="/prospecting", tags=["Prospecting"])
api_router.include_router(users.router, prefix="/users", tags=["User Management"])