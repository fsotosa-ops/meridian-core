import hashlib
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from app.db.supabase_client import get_supabase
from app.core.config import settings

api_key_header = APIKeyHeader(name="X-Meridian-Key", auto_error=False)

async def get_current_user(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail="X-Meridian-Key faltante")
    
    # 1. Limpiamos la llave
    api_key = api_key.strip()
    
    # 2. CONCATENACIÓN CRÍTICA
    # Si settings.API_SECRET_KEY está vacío aquí, el hash será erróneo.
    string_to_hash = f"{api_key}{settings.API_SECRET_KEY}"
    
    # DEBUG: Verifica que esto no sea un string vacío en tu terminal
    # print(f"DEBUG: Secreto cargado -> {settings.API_SECRET_KEY}")
    
    incoming_hash = hashlib.sha256(string_to_hash.encode()).hexdigest()
    print(f"DEBUG: Buscando hash -> {incoming_hash}")
    
    # 3. Consulta a Supabase
    supabase = get_supabase()
    user = supabase.schema("meridian-agent").table("users") \
        .select("*") \
        .eq("hashed_api_key", incoming_hash) \
        .execute()
    
    if not user.data:
        raise HTTPException(status_code=403, detail="X-Meridian-Key inválida o expirada")
        
    return user.data[0]