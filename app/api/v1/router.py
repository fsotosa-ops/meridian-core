from fastapi import APIRouter
from app.api.v1.endpoints import enrich

api_router = APIRouter()
# Aquí puedes ir sumando más módulos (analytics, users, etc.)
api_router.include_router(enrich.router, prefix="/prospecting", tags=["Prospecting"])