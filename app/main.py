from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(title="Meridian Core API", version="3.0.0")

# Conectamos el router principal siguiendo el estándar
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "operational"}