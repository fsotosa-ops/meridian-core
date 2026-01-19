import vecs
from app.core.config import settings

class MeridianVectorStore:
    def __init__(self, user_id: str):
        # Conexión directa a la DB para pgvector
        self.engine = vecs.create_client(settings.SUPABASE_DB_URL)
        # Colección aislada por usuario en el esquema meridian-agent
        self.collection = self.engine.get_or_create_collection(
            name=f"mem_{user_id}", 
            dimension=768 # Dimensión para embeddings de Gemini
        )

    def get_similar_context(self, current_profile: str) -> str:
        """Busca en la memoria vectorial perfiles similares ya aprobados"""
        similar = self.collection.query(
            data=current_profile, 
            limit=3, 
            filters={"status": {"$eq": "approved"}}
        )
        if not similar:
            return "No hay antecedentes previos para este tipo de lead."
        
        return "\n".join([f"Caso previo: {s.metadata['reason']}" for s in similar])