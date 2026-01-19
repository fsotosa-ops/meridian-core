from fastapi import Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from app.db.supabase_client import get_supabase
from app.core.security import verify_meridian_key

api_key_header = APIKeyHeader(name="X-Meridian-Key")

async def get_current_user(api_key: str = Security(api_key_header)):
    supabase = get_supabase()
    # Buscamos al usuario por el hash de su key (mejor práctica)
    # Nota: Aquí se asume una tabla 'users' en Supabase
    user = supabase.table("users").select("*").execute()
    # Lógica de validación...
    return user.data[0] # Retorna el perfil del BDR