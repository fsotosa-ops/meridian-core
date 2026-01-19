import secrets
import hashlib
from fastapi import APIRouter, HTTPException
from app.db.supabase_client import get_supabase
from app.schemas.user import APIKeyResponse, UserBase
from app.core.config import settings

router = APIRouter()

@router.post("/generate-key", response_model=APIKeyResponse)
async def create_user_and_key(user_data: UserBase):
    supabase = get_supabase()
    
    # 1. Generamos la llave física que usará el BDR (sk_live_...)
    raw_key = f"sk_live_{secrets.token_urlsafe(32)}"
    
    # 2. Generamos el hash usando el API_SECRET_KEY del servidor como 'salt'
    # Esto asegura que si roban la DB, no pueden usar las llaves sin tu secreto del .env
    string_to_hash = f"{raw_key}{settings.API_SECRET_KEY}"
    hashed_key = hashlib.sha256(string_to_hash.encode()).hexdigest()
    
    # 3. Guardar en el esquema 'meridian-agent' de Supabase
    try:
        supabase.schema("meridian-agent").table("users").insert({
            "email": user_data.email,
            "hashed_api_key": hashed_key,
            "plan_type": user_data.plan_type
        }).execute()
        
        return {
            "email": user_data.email,
            "api_key": raw_key,
            "note": "⚠️ GUARDA ESTA LLAVE. No se volverá a mostrar por seguridad."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al registrar usuario: {str(e)}")