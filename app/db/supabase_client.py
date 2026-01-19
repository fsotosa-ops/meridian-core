# app/db/supabase_client.py
from supabase import create_client, Client
from app.core.config import settings

def get_supabase() -> Client:
    # Inicialización limpia sin opciones para evitar conflictos de versión
    return create_client(
        settings.SUPABASE_URL, 
        settings.SUPABASE_SERVICE_KEY
    )