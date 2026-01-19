from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Infraestructura Meridian
    SERPER_API_KEY: str
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str
    SUPABASE_DB_URL: str # Formato: postgresql://postgres:[pass]@[host]:5432/postgres
    PROXY_URL: str | None = None
    
    # Seguridad de la API
    API_SECRET_KEY: str # Para validaciones internas si fuera necesario

    class Config:
        env_file = ".env"

settings = Settings()