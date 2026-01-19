-- 1. Habilitar extensiones necesarias
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "pgcrypto"; -- Asegura la disponibilidad de gen_random_uuid()

-- 2. Crear el esquema específico para el agente
CREATE SCHEMA IF NOT EXISTS "meridian-agent";

-- 3. Tabla de Usuarios (BDRs) con ID autogenerado
CREATE TABLE "meridian-agent".users (
    -- Cambio clave: Se usa gen_random_uuid() para no depender de la sesión de Auth de Supabase
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    hashed_api_key TEXT NOT NULL, -- SHA-256 de la sk_live_...
    plan_type TEXT DEFAULT 'free',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Tabla de Memoria Vectorial (Para el RAG)
CREATE TABLE "meridian-agent".leads_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES "meridian-agent".users(id),
    content TEXT, -- Texto crudo del perfil
    metadata JSONB, -- {name, company, role, reason}
    embedding VECTOR(768), -- Tamaño para modelos de Google Gemini
    status TEXT DEFAULT 'validated',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Índice de búsqueda para vectores (HNSW para velocidad)
CREATE INDEX ON "meridian-agent".leads_memory USING hnsw (embedding vector_cosine_ops);

-- 6. Función para búsqueda de similitud (usada por el agente)
CREATE OR REPLACE FUNCTION "meridian-agent".match_leads (
  query_embedding VECTOR(768),
  match_threshold FLOAT,
  match_count INT,
  p_user_id UUID
)
RETURNS TABLE (
  id UUID,
  content TEXT,
  metadata JSONB,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    lm.id,
    lm.content,
    lm.metadata,
    1 - (lm.embedding <=> query_embedding) AS similarity
  FROM "meridian-agent".leads_memory lm
  WHERE lm.user_id = p_user_id 
    AND 1 - (lm.embedding <=> query_embedding) > match_threshold
  ORDER BY similarity DESC
  LIMIT match_count;
END;
$$;

-- 7. PERMISOS DE SEGURIDAD (Esenciales para evitar el error 42501)
-- Otorgar uso del esquema a los roles de la API
GRANT USAGE ON SCHEMA "meridian-agent" TO anon, authenticated, service_role;

-- Otorgar todos los permisos sobre las tablas existentes al rol de servicio
GRANT ALL ON ALL TABLES IN SCHEMA "meridian-agent" TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA "meridian-agent" TO service_role;

-- Asegurar que las tablas futuras también tengan permisos automáticos
ALTER DEFAULT PRIVILEGES IN SCHEMA "meridian-agent" 
GRANT ALL ON TABLES TO service_role;