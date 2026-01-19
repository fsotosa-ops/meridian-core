# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict # <--- Cambio aquí

class Settings(BaseSettings):
    SERPER_API_KEY: str
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str
    SUPABASE_DB_URL: str
    API_SECRET_KEY: str
    SUPABASE_JWKS_URL: str | None = None
    PROXY_URL: str | None = None

    # Usamos model_config (estándar de Pydantic V2)
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()